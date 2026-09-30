import json
import os
from pathlib import Path
from PIL import Image, ImageDraw

def get_color(text):
    text = text.lower()
    if "black" in text: return (30, 30, 30)
    if "white" in text: return (240, 240, 240)
    if "gray" in text or "silver" in text or "stainless" in text: return (160, 160, 160)
    if "red" in text: return (200, 40, 40)
    if "blue" in text: return (40, 40, 200)
    if "green" in text: return (40, 200, 40)
    if "cyan" in text: return (40, 200, 200)
    if "gold" in text: return (218, 165, 32)
    if "purple" in text: return (128, 0, 128)
    return (100, 100, 100) # default

def main():
    data_path = Path("d:/Third Year/DL/CP/trustagent/data/generated/generated_records.json")
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    base_dir = Path("d:/Third Year/DL/CP/trustagent")
    img_dir = base_dir / "images"
    img_dir.mkdir(exist_ok=True)
    
    generated = set()
    
    for r in records:
        if r["visually_verifiable"] and r["sources"]["image_path"]:
            img_path = r["sources"]["image_path"]
            abs_path = base_dir / img_path
            
            if abs_path in generated:
                continue
                
            claim_text = r["sources"]["text"]
            
            is_altered = "altered_" in abs_path.name
            
            color = (128, 128, 128)
            label = "Unknown Color"
            
            if not is_altered:
                color = get_color(claim_text)
                label = claim_text
            else:
                # Contradictory image should be a totally different color, e.g. bright orange
                color = (255, 165, 0)
                label = "Bright Orange"
                
            img = Image.new('RGB', (224, 224), color=color)
            draw = ImageDraw.Draw(img)
            draw.text((10, 100), label, fill=(0,0,0) if sum(color) > 384 else (255,255,255))
            
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(abs_path)
            generated.add(abs_path)
            
    print(f"Generated {len(generated)} visual attribute images.")

if __name__ == "__main__":
    main()
