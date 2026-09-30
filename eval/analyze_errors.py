import json
import torch
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from trustagent.models.consistency_net.model import MultiModalConsistencyNet
from trustagent.models.trust_score_net.train import TrustScoreNet
from trustagent.models.text_verifier.verifier import verify_text
from trustagent.models.image_verifier.verifier import verify_image
from trustagent.models.consistency_net.features import build_features
from trustagent.models.trust_score_net.metadata_lookup import get_record_features

def get_true_claim(entity, attribute):
    from trustagent.data.generator.seed_data import data as seed_data
    for product in seed_data:
        if product["entity"] == entity:
            if attribute in product["attributes"]:
                attr = product["attributes"][attribute]
                unit_str = f" {attr['unit']}" if attr.get("unit") else ""
                return f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_str}."
    return None

def main():
    # Load human ratings
    ratings_path = Path("d:/Third Year/DL/CP/trustagent/eval/human_ratings.json")
    with open(ratings_path, "r", encoding="utf-8") as f:
        human_ratings = json.load(f)
        
    data_path = Path("d:/Third Year/DL/CP/trustagent/data/generated/generated_records.json")
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    record_dict = {r["record_id"]: r for r in records}
    
    # Load Models
    cons_net = MultiModalConsistencyNet(input_dim=5, hidden_dim=64)
    cons_net.load_state_dict(torch.load("d:/Third Year/DL/CP/trustagent/models/consistency_net/checkpoint.pt"))
    cons_net.eval()
    
    ts_net = TrustScoreNet()
    ts_net.load_state_dict(torch.load("d:/Third Year/DL/CP/trustagent/models/trust_score_net/checkpoint.pt"))
    ts_net.eval()
    
    results = []
    
    for rating in human_ratings:
        r_id = rating["record_id"]
        h_score = rating["human_score"]
        notes = rating["rater_notes"]
        
        record = record_dict[r_id]
        claim = get_true_claim(record["entity"], record["attribute"])
        
        evidence_text = record["sources"]["text"]
        image_path = record["sources"]["image_path"]
        is_visual = record.get("visually_verifiable", False)
        
        t_label, t_score = verify_text(claim, evidence_text)
        i_label, i_score = verify_image(claim, image_path, visually_verifiable=is_visual)
        
        features = build_features(t_label, t_score, i_label, i_score)
        features_tensor = torch.tensor([features], dtype=torch.float32)
        
        with torch.no_grad():
            consistency_score = cons_net(features_tensor).item()
            
        evidence_available = features[4]
        
        # We need a stable random avg_conf just like evaluate_human.py
        import hashlib
        h = int(hashlib.md5(r_id.encode()).hexdigest(), 16)
        import random
        random.seed(h)
        avg_conf = random.uniform(0.5, 1.0) if evidence_available else 0.0
        
        source_reliability, action_risk = get_record_features(r_id)
        
        ts_features = torch.tensor([[consistency_score, evidence_available, avg_conf, source_reliability, action_risk]], dtype=torch.float32)
        
        with torch.no_grad():
            trust_score_pred = ts_net(ts_features).item()
            
        abs_err = abs(h_score - trust_score_pred)
        
        results.append({
            "record_id": r_id,
            "human_score": h_score,
            "pred_score": trust_score_pred,
            "abs_error": abs_err,
            "t_label": t_label,
            "t_score": t_score,
            "notes": notes
        })
        
    results.sort(key=lambda x: x["abs_error"], reverse=True)
    
    print(f"{'Record ID':<40} | {'Human':<6} | {'Pred':<6} | {'Error':<6} | {'T_Lbl':<10} | {'T_Scr':<6} | Notes")
    print("-" * 120)
    for r in results:
        print(f"{r['record_id']:<40} | {r['human_score']:<6.1f} | {r['pred_score']:<6.1f} | {r['abs_error']:<6.1f} | {r['t_label']:<10} | {r['t_score']:<6.3f} | {r['notes']}")

if __name__ == "__main__":
    main()
