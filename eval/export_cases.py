import json
import random
from pathlib import Path

def main():
    data_path = Path("d:/Third Year/DL/CP/trustagent/data/generated/generated_records.json")
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    t_res_path = Path("d:/Third Year/DL/CP/trustagent/eval/results/phase4_text_verifier.json")
    with open(t_res_path, "r", encoding="utf-8") as f:
        t_res = {r["record_id"]: r["pred_label"] for r in json.load(f)["predictions"]}
        
    i_res_path = Path("d:/Third Year/DL/CP/trustagent/eval/results/phase4_image_verifier.json")
    with open(i_res_path, "r", encoding="utf-8") as f:
        i_res = {r["record_id"]: r["pred_label"] for r in json.load(f)["predictions"]}

    random.seed(4242)
    sample_records = random.sample(records, 25)

    from trustagent.data.generator.seed_data import data as seed_data
    def get_true_claim(entity, attribute):
        for product in seed_data:
            if product['entity'] == entity:
                if attribute in product['attributes']:
                    attr = product['attributes'][attribute]
                    unit_str = f" {attr['unit']}" if attr.get('unit') else ""
                    return f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_str}."
        return None

    output = "# Human Ratings Worksheet\n\nPlease assign a 0-100 score for each record below based on whether the evidence supports the claim (100 = perfectly supported, 0 = direct contradiction, 50 = no evidence or unclear).\n\n"

    for i, r in enumerate(sample_records):
        claim = get_true_claim(r['entity'], r['attribute'])
        text_ev = r['sources']['text']
        img_ev = r['sources']['image_path']
        
        t_label = t_res.get(r['record_id'], "NOT_EVALUATED")
        i_label = i_res.get(r['record_id'], "NO_EVIDENCE") # Image verifier only evaluated visual ones
        
        output += f"### Record {i+1}: {r['record_id']}\n"
        output += f"**Claim**: {claim}\n\n"
        output += f"**Text Evidence**: {text_ev}\n"
        output += f"**Text Verifier Output**: {t_label}\n\n"
        output += f"**Image Evidence Path**: {img_ev}\n"
        output += f"**Image Verifier Output**: {i_label}\n\n"
        output += f"**Your Score (0-100)**: \n"
        output += f"**Your Notes**: \n\n---\n\n"
        
    out_path = Path("d:/Third Year/DL/CP/trustagent/eval/cases_to_rate.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
        
    print(f"Generated {out_path}")

if __name__ == "__main__":
    main()
