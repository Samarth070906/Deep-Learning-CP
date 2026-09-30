import json
import random
import os
import sys
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from trustagent.models.image_verifier.verifier import verify_image
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
    
    print(f"Evaluating Image Verifier on {len(test_records)} test records...")
    
    for i, record in enumerate(test_records):
        claim = get_true_claim(record["entity"], record["attribute"])
        if not claim: continue
            
        image_path = record["sources"]["image_path"]
        visually_verifiable = record.get("visually_verifiable", False)
        gt_label = record["label"] # CONSISTENT or CONTRADICTORY
        
        pred_label, pred_score = verify_image(claim, image_path, visually_verifiable=visually_verifiable)
        
        # Only evaluate on records that are actually visually verifiable for accuracy/F1
        if visually_verifiable and image_path:
            true_binary = 1 if gt_label == "CONSISTENT" else 0
            
            if pred_label == "SUPPORT":
                pred_binary = 1
            else:
                pred_binary = 0
                
            y_true.append(true_binary)
            y_pred.append(pred_binary)
            
        results.append({
            "record_id": record["record_id"],
            "visually_verifiable": visually_verifiable,
            "gt_label": gt_label,
            "pred_label": pred_label,
            "pred_score": pred_score
        })
        
        if (i+1) % 50 == 0:
            print(f"Processed {i+1}/{len(test_records)}")
            
    if len(y_true) > 0:
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
    else:
        acc = 0.0
        f1 = 0.0
    
    out_dir = Path(__file__).resolve().parent.parent.parent / "eval" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = out_dir / "phase4_image_verifier.json"
    
    output = {
        "metrics": {
            "accuracy": acc,
            "f1": f1,
            "evaluated_samples": len(y_true)
        },
        "predictions": results
    }
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        
    print(f"Saved evaluation results to {out_file}")
    print(f"Evaluated on {len(y_true)} visually verifiable samples.")
    print(f"Accuracy: {acc:.4f}, F1-Score: {f1:.4f}")

if __name__ == "__main__":
    main()
