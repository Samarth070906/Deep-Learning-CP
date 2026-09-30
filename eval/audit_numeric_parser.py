import json
import re
from pathlib import Path

def main():
    data_path = Path("d:/Third Year/DL/CP/trustagent/data/generated/generated_records.json")
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    def extract_last_number(text):
        if not text: return None
        matches = re.findall(r"\d+\.\d+|\d+", text)
        return float(matches[-1]) if matches else None

    from trustagent.data.generator.seed_data import data as seed_data
    def get_true_claim(entity, attribute):
        for product in seed_data:
            if product["entity"] == entity:
                if attribute in product["attributes"]:
                    attr = product["attributes"][attribute]
                    unit_str = f" {attr['unit']}" if attr.get("unit") else ""
                    return f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_str}."
        return None

    parsed_count = 0
    false_positives = 0
    
    for r in records:
        claim = get_true_claim(r["entity"], r["attribute"])
        ev = r["sources"]["text"]
        
        vc = extract_last_number(claim)
        ve = extract_last_number(ev)
        
        if vc is not None and ve is not None:
            parsed_count += 1
            entity = r["entity"]
            entity_nums = re.findall(r"\d+\.\d+|\d+", entity)
            if entity_nums:
                e_num = float(entity_nums[-1])
                try:
                    true_val_str = seed_data[[p["entity"] for p in seed_data].index(entity)]["attributes"].get(r["attribute"], {}).get("value", -999)
                    true_val = float(true_val_str)
                    if vc == e_num and true_val != e_num:
                        false_positives += 1
                except ValueError:
                    if vc == e_num:
                        false_positives += 1
                        
    print(f"Total parsed with old regex: {parsed_count}")
    print(f"False positives (extracted product digit instead of value): {false_positives}")

if __name__ == "__main__":
    main()
