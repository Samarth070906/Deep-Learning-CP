import torch
from PIL import Image
import os
from transformers import CLIPProcessor, CLIPModel

_model_name = "openai/clip-vit-base-patch32"
_processor = None
_model = None

def _get_model():
    global _processor, _model
    if _model is None:
        _processor = CLIPProcessor.from_pretrained(_model_name)
        _model = CLIPModel.from_pretrained(_model_name)
        _model.eval()
    return _processor, _model

def verify_image(claim: str, image_path: str, threshold_support: float = 0.25, threshold_contradict: float = 0.18, visually_verifiable: bool = True) -> tuple[str, float]:
    """
    Verifies a claim against an image using CLIP cosine similarity.
    
    Returns:
        (label, score)
        label is one of: "SUPPORT", "CONTRADICT", "NO_EVIDENCE"
    """
    if not visually_verifiable or not image_path:
        return "NO_EVIDENCE", 0.0
        
    abs_path = os.path.join("d:\\Third Year\\DL\\CP\\trustagent", image_path)
    if not os.path.exists(abs_path):
        # We will no longer generate blank images here. We expect real images to be present.
        return "NO_EVIDENCE", 0.0

    try:
        image = Image.open(abs_path)
    except Exception:
        return "NO_EVIDENCE", 0.0

    processor, model = _get_model()
    
    inputs = processor(text=[claim], images=image, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    image_embeds = outputs.image_embeds
    text_embeds = outputs.text_embeds
    
    image_embeds = image_embeds / image_embeds.norm(p=2, dim=-1, keepdim=True)
    text_embeds = text_embeds / text_embeds.norm(p=2, dim=-1, keepdim=True)
    
    cosine_sim = torch.matmul(text_embeds, image_embeds.t()).item()
    
    if cosine_sim > threshold_support:
        return "SUPPORT", cosine_sim
    elif cosine_sim < threshold_contradict:
        return "CONTRADICT", cosine_sim
    else:
        return "NO_EVIDENCE", cosine_sim
