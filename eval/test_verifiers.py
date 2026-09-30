import json
import random
import os
import sys
from pathlib import Path
from PIL import Image

# Add trustagent to path if needed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from trustagent.models.text_verifier.verifier import verify_text
from trustagent.models.image_verifier.verifier import verify_image
from trustagent.data.generator.seed_data import data as seed_data

def load_data():
    data_path = Path(__file__).resolve().parent.parent / "data" / "generated" / "generated_records.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_true_claim(entity, attribute):
    for product in seed_data:
        if product["entity"] == entity:
            if attribute in product["attributes"]:
                attr = product["attributes"][attribute]
                return f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']} {attr['unit']}."
    return None

def evaluate_text_verifier(test_set):
    print(f"\n--- Evaluating Text Verifier (Zero-shot NLI) on {len(test_set)} samples ---")
    
    correct = 0
    predictions = []
    labels = []
    
    for i, record in enumerate(test_set):
        evidence_text = record["sources"]["text"]
        label = record["label"]
        
        # Construct true claim from seed data
        claim = get_true_claim(record["entity"], record["attribute"])
        if not claim:
            continue
            
        pred_label, score = verify_text(claim, evidence_text)
        
        # Map our prediction to CONSISTENT/CONTRADICTORY for accuracy comparison
        if pred_label == "SUPPORT":
            mapped_pred = "CONSISTENT"
        elif pred_label == "CONTRADICT":
            mapped_pred = "CONTRADICTORY"
        else:
            mapped_pred = "NO_EVIDENCE" # Will count as incorrect for this binary test
            
        if mapped_pred == label:
            correct += 1
            
        predictions.append(mapped_pred)
        labels.append(label)
        
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1}/{len(test_set)} text samples")
            
    acc = correct / len(labels) if labels else 0
    print(f"Text Verifier Accuracy: {acc:.4f} ({correct}/{len(labels)})")
    
    # Calculate simple F1 for CONSISTENT class
    tp = sum(1 for p, l in zip(predictions, labels) if p == "CONSISTENT" and l == "CONSISTENT")
    fp = sum(1 for p, l in zip(predictions, labels) if p == "CONSISTENT" and l != "CONSISTENT")
    fn = sum(1 for p, l in zip(predictions, labels) if p != "CONSISTENT" and l == "CONSISTENT")
    
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    
    print(f"Text Verifier F1 (CONSISTENT): {f1:.4f}")
    return acc, f1

def evaluate_image_verifier(train_set, test_set):
    print(f"\n--- Calibrating and Evaluating Image Verifier (CLIP) ---")
    
    # Calibration
    print(f"Calibrating on {len(train_set)} samples...")
    similarities = []
    train_labels = []
    
    no_evidence_count = 0
    
    for i, record in enumerate(train_set):
        claim = get_true_claim(record["entity"], record["attribute"])
        image_path = record["sources"]["image_path"]
        is_visual = record.get("visually_verifiable", False)
        
        if not claim or not image_path:
            continue
            
        _, score = verify_image(claim, image_path, 0.0, 0.0, is_visual)
        if not is_visual:
            no_evidence_count += 1
            continue
            
        similarities.append(score)
        train_labels.append(record["label"])
        
    cons_sims = [s for s, l in zip(similarities, train_labels) if l == "CONSISTENT"]
    contra_sims = [s for s, l in zip(similarities, train_labels) if l == "CONTRADICTORY"]
    
    avg_cons = sum(cons_sims) / len(cons_sims) if cons_sims else 0
    avg_contra = sum(contra_sims) / len(contra_sims) if contra_sims else 0
    
    print(f"Avg similarity for CONSISTENT: {avg_cons:.4f}")
    print(f"Avg similarity for CONTRADICTORY: {avg_contra:.4f}")
    
    # Calculate thresholds (midpoint)
    thresh = (avg_cons + avg_contra) / 2
    support_thresh = thresh + 0.01
    contradict_thresh = thresh - 0.01
    
    print(f"Calibrated threshold_support: {support_thresh:.4f}")
    print(f"Calibrated threshold_contradict: {contradict_thresh:.4f}")
    
    # Evaluation
    print(f"Evaluating on {len(test_set)} samples...")
    correct = 0
    predictions = []
    test_labels_list = []
    
    for i, record in enumerate(test_set):
        claim = get_true_claim(record["entity"], record["attribute"])
        image_path = record["sources"]["image_path"]
        is_visual = record.get("visually_verifiable", False)
        
        if not claim or not image_path:
            continue
            
        pred_label, _ = verify_image(claim, image_path, support_thresh, contradict_thresh, is_visual)
        
        if not is_visual:
            no_evidence_count += 1
            continue
        
        mapped_pred = "CONSISTENT" if pred_label == "SUPPORT" else "CONTRADICTORY" if pred_label == "CONTRADICT" else "NO_EVIDENCE"
        
        if mapped_pred == record["label"]:
            correct += 1
            
        predictions.append(mapped_pred)
        test_labels_list.append(record["label"])
            
    total_records = len(train_set) + len(test_set)
    print(f"NO_EVIDENCE rate (non-visual attributes): {no_evidence_count}/{total_records} ({no_evidence_count/total_records*100:.1f}%)")
    
    acc = correct / len(test_labels_list) if test_labels_list else 0
    print(f"Image Verifier Accuracy (on visual attributes): {acc:.4f} ({correct}/{len(test_labels_list)})")
    
    tp = sum(1 for p, l in zip(predictions, test_labels_list) if p == "CONSISTENT" and l == "CONSISTENT")
    fp = sum(1 for p, l in zip(predictions, test_labels_list) if p == "CONSISTENT" and l != "CONSISTENT")
    fn = sum(1 for p, l in zip(predictions, test_labels_list) if p != "CONSISTENT" and l == "CONSISTENT")
    
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    
    print(f"Image Verifier F1 (CONSISTENT): {f1:.4f}")
    return acc, f1

def main():
    records = load_data()
    random.seed(42)
    random.shuffle(records)
    
    # 20% held-out slice
    split_idx = int(len(records) * 0.8)
    train_set = records[:split_idx] 
    test_set = records[split_idx:]  
    
    print(f"Total records: {len(records)}, Train set (calibration): {len(train_set)}, Test set (eval): {len(test_set)}")
    
    evaluate_text_verifier(test_set)
    evaluate_image_verifier(train_set, test_set)
    
    print("\nPhase 4 Evaluation Complete.")

if __name__ == "__main__":
    main()
