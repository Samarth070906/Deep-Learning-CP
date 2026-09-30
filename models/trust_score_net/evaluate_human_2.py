import json
import torch
import random
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error
import sys
import hashlib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from trustagent.models.consistency_net.model import MultiModalConsistencyNet
from trustagent.models.trust_score_net.train import TrustScoreNet
from trustagent.models.text_verifier.verifier import verify_text
from trustagent.models.image_verifier.verifier import verify_image
from trustagent.models.consistency_net.features import build_features
from trustagent.models.trust_score_net.metadata_lookup import get_record_features
from trustagent.models.trust_score_net.numeric_parser import get_numeric_deviation

def get_true_claim_and_unit(entity, attribute):
    from trustagent.data.generator.seed_data import data as seed_data
    for product in seed_data:
        if product["entity"] == entity:
            if attribute in product["attributes"]:
                attr = product["attributes"][attribute]
                unit_str = attr.get('unit', '')
                unit_display = f" {unit_str}" if unit_str else ""
                claim = f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_display}."
                return claim, unit_str
    return None, None

def main():
    ratings_path = Path("d:/Third Year/DL/CP/trustagent/eval/human_ratings_2.json")
    with open(ratings_path, "r", encoding="utf-8") as f:
        human_ratings = json.load(f)
        
    data_path = Path("d:/Third Year/DL/CP/trustagent/data/generated/generated_records.json")
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    record_dict = {r["record_id"]: r for r in records}
    
    cons_net = MultiModalConsistencyNet(input_dim=5, hidden_dim=64)
    cons_net.load_state_dict(torch.load("d:/Third Year/DL/CP/trustagent/models/consistency_net/checkpoint.pt"))
    cons_net.eval()
    
    ts_net = TrustScoreNet()
    ts_net.load_state_dict(torch.load("d:/Third Year/DL/CP/trustagent/models/trust_score_net/checkpoint.pt"))
    ts_net.eval()
    
    test_preds = []
    test_actual = []
    results = []
    
    for rating in human_ratings:
        r_id = rating["record_id"]
        h_score = rating["human_score"]
        
        record = record_dict[r_id]
        claim, unit = get_true_claim_and_unit(record["entity"], record["attribute"])
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
        
        num_dev = get_numeric_deviation(claim, evidence_text, unit)
        
        h = int(hashlib.md5(r_id.encode()).hexdigest(), 16)
        random.seed(h)
        avg_conf = random.uniform(0.5, 1.0) if evidence_available else 0.0
        source_reliability, action_risk = get_record_features(r_id)
        
        ts_features = torch.tensor([[consistency_score, evidence_available, avg_conf, source_reliability, action_risk, num_dev]], dtype=torch.float32)
        
        with torch.no_grad():
            trust_score_pred = ts_net(ts_features).item()
            
        test_preds.append(trust_score_pred)
        test_actual.append(h_score)
        
        results.append({
            "record_id": r_id,
            "human_score": h_score,
            "pred_score": trust_score_pred,
            "abs_error": abs(h_score - trust_score_pred),
            "num_dev": num_dev,
            "t_label": t_label,
            "c_score": consistency_score,
            "e_avail": evidence_available,
            "avg_conf": avg_conf,
            "rel": source_reliability,
            "risk": action_risk
        })
        
    pearson_corr, _ = pearsonr(test_actual, test_preds)
    mae = mean_absolute_error(test_actual, test_preds)
    
    print("\n--- Real Human Evaluation Results (6-dim Unit Aware) ---")
    print(f"Evaluated on {len(human_ratings)} human-labeled samples.")
    print(f"Pearson Correlation: {pearson_corr:.4f}")
    print(f"MAE: {mae:.4f}\n")
    
    print(f"{'Record ID':<40} | {'Human':<6} | {'Pred':<6} | {'Error':<6} | {'Dev':<6} | {'T_Lbl':<10} | {'C_Scr':<6} | {'E_Av':<5}")
    print("-" * 105)
    results.sort(key=lambda x: x["abs_error"], reverse=True)
    for r in results:
        print(f"{r['record_id']:<40} | {r['human_score']:<6.1f} | {r['pred_score']:<6.1f} | {r['abs_error']:<6.1f} | {r['num_dev']:<6.3f} | {r['t_label']:<10} | {r['c_score']:<6.3f} | {r['e_avail']:<5.1f}")
        
    # Diagnose SUPPORT cases specifically
    print("\n--- SUPPORT Case Diagnosis ---")
    for r in results:
        if r['t_label'] == 'SUPPORT':
            print(f"ID: {r['record_id']}")
            print(f"  Human Score: {r['human_score']}")
            print(f"  Pred Score: {r['pred_score']}")
            print(f"  Consistency Score: {r['c_score']:.4f}")
            print(f"  Evidence Avail: {r['e_avail']:.1f}")
            print(f"  Avg Conf: {r['avg_conf']:.4f}")
            print(f"  Source Rel: {r['rel']:.4f}")
            print(f"  Action Risk: {r['risk']:.4f}")
            print(f"  Numeric Dev: {r['num_dev']:.4f}")
            print()

if __name__ == "__main__":
    main()
