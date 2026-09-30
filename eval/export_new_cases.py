import json
import random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from trustagent.models.text_verifier.verifier import verify_text
from trustagent.models.image_verifier.verifier import verify_image
from trustagent.models.trust_score_net.evaluate_human import get_true_claim_and_unit

def main():
    ratings_path = Path("d:/Third Year/DL/CP/trustagent/eval/human_ratings.json")
    with open(ratings_path, "r", encoding="utf-8") as f:
        existing_ratings = json.load(f)
    existing_ids = set(r["record_id"] for r in existing_ratings)
    
    data_path = Path("d:/Third Year/DL/CP/trustagent/data/generated/generated_records.json")
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    random.seed(555) # New seed for new selection
    
    # We want ~20 cases: mix of exact match, small diff, large diff, categorical.
    # We need to compute text verifier outputs to find the mix.
    # To save time, we'll iterate and collect until we hit our quota.
    
    selected_records = []
    
    cat_quota = 3
    exact_quota = 7 # heavily bias towards exact matches (single modality SUPPORT)
    small_dev_quota = 5
    large_dev_quota = 5
    
    for r in records:
        r_id = r["record_id"]
        if r_id in existing_ids:
            continue
            
        claim_text, unit = get_true_claim_and_unit(r["entity"], r["attribute"])
        ev_text = r["sources"]["text"]
        
        # We need to know if it's an exact match or deviation
        from trustagent.models.trust_score_net.numeric_parser import get_numeric_deviation
        num_dev = get_numeric_deviation(claim_text, ev_text, unit)
        
        # Classify record
        category = None
        if num_dev == -1.0:
            if cat_quota > 0:
                category = "cat"
                cat_quota -= 1
        elif num_dev == 0.0:
            if exact_quota > 0:
                category = "exact"
                exact_quota -= 1
        elif 0.0 < num_dev <= 0.15:
            if small_dev_quota > 0:
                category = "small"
                small_dev_quota -= 1
        elif num_dev > 0.15:
            if large_dev_quota > 0:
                category = "large"
                large_dev_quota -= 1
                
        if category:
            # Let's get the verifier outputs
            image_path = r["sources"]["image_path"]
            is_visual = r.get("visually_verifiable", False)
            t_label, _ = verify_text(claim_text, ev_text)
            i_label, _ = verify_image(claim_text, image_path, visually_verifiable=is_visual)
            
            selected_records.append({
                "record_id": r_id,
                "claim": claim_text,
                "text_ev": ev_text,
                "t_label": t_label,
                "img_ev": image_path,
                "i_label": i_label,
                "category": category
            })
            
        if cat_quota == 0 and exact_quota == 0 and small_dev_quota == 0 and large_dev_quota == 0:
            break
            
    # Write to cases_to_rate_2.md
    out_path = Path("d:/Third Year/DL/CP/trustagent/eval/cases_to_rate_2.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Human Ratings Worksheet - FRESH SET\n\n")
        f.write("Please assign a 0-100 score for each record below based on whether the evidence supports the claim (100 = perfectly supported, 0 = direct contradiction, 50 = no evidence or unclear).\n\n")
        
        for i, sr in enumerate(selected_records):
            f.write(f"### Record {i+1}: {sr['record_id']}\n")
            f.write(f"**Claim**: {sr['claim']}\n\n")
            f.write(f"**Text Evidence**: {sr['text_ev']}\n")
            f.write(f"**Text Verifier Output**: {sr['t_label']}\n\n")
            f.write(f"**Image Evidence Path**: {sr['img_ev']}\n")
            f.write(f"**Image Verifier Output**: {sr['i_label']}\n\n")
            f.write(f"**Your Score (0-100)**: \n")
            f.write(f"**Your Notes**: \n\n")
            f.write("---\n\n")

if __name__ == "__main__":
    main()
