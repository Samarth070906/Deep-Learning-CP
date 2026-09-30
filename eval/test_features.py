import json
from trustagent.models.consistency_net.features import build_features

def main():
    print("--- NO_EVIDENCE Exclusion Unit Test ---")
    
    # 3 mock examples based on real behavior of non-visual attributes
    # For a non-visual attribute, image_verifier returns ("NO_EVIDENCE", 0.0)
    
    records = [
        {"id": "SuperPhone_X_price_00001", "t_label": "SUPPORT", "t_score": 0.85, "i_label": "NO_EVIDENCE", "i_score": 0.0},
        {"id": "MegaTablet_Pro_storage_00025", "t_label": "CONTRADICT", "t_score": 0.92, "i_label": "NO_EVIDENCE", "i_score": 0.0},
        {"id": "UltraLaptop_Air_ram_00104", "t_label": "SUPPORT", "t_score": 0.60, "i_label": "NO_EVIDENCE", "i_score": 0.0},
    ]
    
    for r in records:
        features = build_features(r["t_label"], r["t_score"], r["i_label"], r["i_score"])
        # features = [text_score, image_score, num_modalities, pairwise_disagreement]
        text_score, image_score, num_modalities, pairwise_disagreement = features
        
        print(f"Record: {r['id']}")
        print(f"  Inputs: text_label={r['t_label']}, image_label={r['i_label']}")
        print(f"  -> num_modalities_available computed: {num_modalities}")
        print(f"  -> pairwise_disagreement_flag computed: {pairwise_disagreement}")
        assert num_modalities == 1.0, "num_modalities_available should be 1.0 (text only)"
        assert pairwise_disagreement == 0.0, "pairwise_disagreement_flag should be 0.0"
        print("  [PASS]")
        print()
        
    # Also test one where both are present and disagree
    print("Testing a record with both modalities present and disagreeing:")
    r = {"id": "SuperPhone_X_color_00050", "t_label": "SUPPORT", "t_score": 0.8, "i_label": "CONTRADICT", "i_score": 0.15}
    f = build_features(r["t_label"], r["t_score"], r["i_label"], r["i_score"])
    print(f"  Inputs: text_label={r['t_label']}, image_label={r['i_label']}")
    print(f"  -> num_modalities_available computed: {f[2]}")
    print(f"  -> pairwise_disagreement_flag computed: {f[3]}")
    assert f[2] == 2.0
    assert f[3] == 1.0
    print("  [PASS]")

if __name__ == "__main__":
    main()
