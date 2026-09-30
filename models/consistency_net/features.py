def build_features(text_label, text_score, image_label, image_score):
    """
    Builds the 4-dim input vector for MultiModalConsistencyNet.
    
    Inputs:
    - text_label: 'SUPPORT', 'CONTRADICT', or 'NO_EVIDENCE'
    - text_score: raw confidence score (or entailment probability)
    - image_label: 'SUPPORT', 'CONTRADICT', or 'NO_EVIDENCE'
    - image_score: raw cosine similarity score
    
    Returns a list of 4 floats:
    [text_score, image_score_or_null, num_modalities, pairwise_disagreement]
    """
    
    num_modalities = 0
    if text_label != "NO_EVIDENCE":
        num_modalities += 1
    if image_label != "NO_EVIDENCE":
        num_modalities += 1
        
    image_score_val = image_score if image_label != "NO_EVIDENCE" else 0.0
    text_score_val = text_score if text_label != "NO_EVIDENCE" else 0.0
    
    # Pairwise disagreement fires ONLY if we have multiple modalities and they disagree
    pairwise_disagreement = 0.0
    if num_modalities == 2:
        if (text_label == "SUPPORT" and image_label == "CONTRADICT") or \
           (text_label == "CONTRADICT" and image_label == "SUPPORT"):
            pairwise_disagreement = 1.0
            
    evidence_available = 1.0 if num_modalities > 0 else 0.0
            
    return [text_score_val, image_score_val, float(num_modalities), pairwise_disagreement, evidence_available]

