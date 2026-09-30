import json
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from trustagent.models.consistency_net.features import build_features
from trustagent.data.generator.seed_data import data as seed_data
from trustagent.models.text_verifier.verifier import verify_text
from trustagent.models.image_verifier.verifier import verify_image

def get_true_claim(entity, attribute):
    for product in seed_data:
        if product["entity"] == entity:
            if attribute in product["attributes"]:
                attr = product["attributes"][attribute]
                unit_str = f" {attr['unit']}" if attr.get("unit") else ""
                return f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_str}."
    return None

class TestNoEvidenceExclusion(unittest.TestCase):
    def setUp(self):
        # Load a few actual records from dataset
        data_path = Path(__file__).resolve().parent.parent / "data" / "generated" / "generated_records.json"
        with open(data_path, "r", encoding="utf-8") as f:
            records = json.load(f)
            
        # Filter for records that are NOT visually verifiable (should trigger NO_EVIDENCE for image)
        self.non_visual_records = [r for r in records if not r.get("visually_verifiable", False)][:3]
        
    def test_no_evidence_features(self):
        print("\n--- Running TestNoEvidenceExclusion ---")
        self.assertTrue(len(self.non_visual_records) >= 3, "Need at least 3 non-visual records for this test.")
        
        for i, record in enumerate(self.non_visual_records):
            claim = get_true_claim(record["entity"], record["attribute"])
            self.assertIsNotNone(claim)
            
            evidence_text = record["sources"]["text"]
            image_path = record["sources"]["image_path"]
            
            # Predict
            t_label, t_score = verify_text(claim, evidence_text)
            
            # This should force NO_EVIDENCE because they are non-visual
            i_label, i_score = verify_image(claim, image_path, visually_verifiable=False)
            
            # Feature build
            features = build_features(t_label, t_score, i_label, i_score)
            
            text_f, image_f, num_mod_f, disagree_f, evidence_avail_f = features
            
            print(f"Record {record['record_id']} - Text: {t_label}, Image: {i_label}")
            print(f"  Features: num_modalities={num_mod_f}, pairwise_disagreement={disagree_f}, evidence_available={evidence_avail_f}")
            
            self.assertEqual(i_label, "NO_EVIDENCE", "Image label must be NO_EVIDENCE")
            self.assertEqual(image_f, 0.0, "Image score must be forced to 0.0 for NO_EVIDENCE")
            
            # Verification logic for NO_EVIDENCE exclusions:
            # num_modalities_available should be 1 if text is present, or 0 if both absent
            expected_mod = 1.0 if t_label != "NO_EVIDENCE" else 0.0
            self.assertEqual(num_mod_f, expected_mod, "num_modalities_available is incorrect")
            
            # evidence_available should be 1.0 if any modality is present
            self.assertEqual(evidence_avail_f, expected_mod, "evidence_available flag is incorrect")
            
            # pairwise_disagreement_flag should be strictly 0.0 if one or more modalities is NO_EVIDENCE
            self.assertEqual(disagree_f, 0.0, "pairwise_disagreement_flag MUST be 0.0 if not exactly 2 modalities present")
            
        print("--- TestNoEvidenceExclusion Passed ---")

if __name__ == "__main__":
    unittest.main()
