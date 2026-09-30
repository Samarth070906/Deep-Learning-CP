import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

_model_name = "cross-encoder/nli-deberta-v3-base" # Fine-tuned NLI model
_tokenizer = None
_model = None

def _get_model():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(_model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(_model_name)
        _model.eval()
    return _tokenizer, _model

def verify_text(claim: str, evidence_text: str) -> tuple[str, float]:
    """
    Verifies a claim against textual evidence using zero-shot NLI.
    
    Returns:
        (label, score)
        label is one of: "SUPPORT", "CONTRADICT", "NO_EVIDENCE"
    """
    if not evidence_text:
        return "NO_EVIDENCE", 0.0

    tokenizer, model = _get_model()
    
    features = tokenizer(claim, evidence_text, padding=True, truncation=True, return_tensors="pt")
    
    with torch.no_grad():
        scores = model(**features).logits
        
    # cross-encoder/nli-deberta-v3-base labels: 0: contradiction, 1: entailment, 2: neutral
    probs = torch.nn.functional.softmax(scores, dim=1)[0]
    
    prob_contradiction = probs[0].item()
    prob_entailment = probs[1].item()
    prob_neutral = probs[2].item()
    
    # Simple max heuristic
    max_prob = max(prob_entailment, prob_contradiction, prob_neutral)
    
    if max_prob == prob_entailment:
        return "SUPPORT", prob_entailment
    elif max_prob == prob_contradiction:
        return "CONTRADICT", prob_contradiction
    else:
        return "NO_EVIDENCE", prob_neutral
