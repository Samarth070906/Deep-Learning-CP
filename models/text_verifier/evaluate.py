import json
import random
import os
import sys
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from trustagent.models.text_verifier.verifier import verify_text
from trustagent.data.generator.seed_data import data as seed_data

def get_true_claim(entity, attribute):
    for product in seed_data:
        if product["entity"] == entity:
            if attribute in product["attributes"]:
                attr = product["attributes"][attribute]
                unit_str = f" {attr['unit']}" if attr.get("unit") else ""
                return f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_str}."
    return None

def main():
    # Fixed random seed
    random.seed(42)
    
    data_path = Path(__file__).resolve().parent.parent.parent / "data" / "generated" / "generated_records.json"
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    random.shuffle(records)
    split_idx = int(len(records) * 0.8)
    test_records = records[split_idx:]
    
    y_true = []
    y_pred = []
    results = []
    
    print(f"Evaluating Text Verifier on {len(test_records)} test records...")
    
    for i, record in enumerate(test_records):
        claim = get_true_claim(record["entity"], record["attribute"])
        if not claim: continue
            
        evidence_text = record["sources"]["text"]
        gt_label = record["label"] # CONSISTENT or CONTRADICTORY
        
        # In our generated data, CONSISTENT implies it should be SUPPORT (1)
        # CONTRADICTORY implies it should be CONTRADICT (0)
        true_binary = 1 if gt_label == "CONSISTENT" else 0
        
        pred_label, pred_score = verify_text(claim, evidence_text)
        
        # If it returns NO_EVIDENCE, we might just count it as incorrect for binary metric purposes
        # or map it. Let's map SUPPORT->1, CONTRADICT->0, NO_EVIDENCE->0 (conservative)
        if pred_label == "SUPPORT":
            pred_binary = 1
        else:
            pred_binary = 0
            
        y_true.append(true_binary)
        y_pred.append(pred_binary)
        
        results.append({
            "record_id": record["record_id"],
            "gt_label": gt_label,
            "pred_label": pred_label,
            "pred_score": pred_score
        })
        
        if (i+1) % 50 == 0:
            print(f"Processed {i+1}/{len(test_records)}")
            
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    out_dir = Path(__file__).resolve().parent.parent.parent / "eval" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = out_dir / "phase4_text_verifier.json"
    
    output = {
        "metrics": {
            "accuracy": acc,
            "f1": f1
        },
        "predictions": results
    }
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        
    print(f"Saved evaluation results to {out_file}")
    print(f"Accuracy: {acc:.4f}, F1-Score: {f1:.4f}")

if __name__ == "__main__":
    main()
