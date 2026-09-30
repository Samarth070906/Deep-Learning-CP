MINOR_DEVIATION_THRESHOLD = 0.15

def get_decision(
    trust_score: float, 
    numeric_deviation: float = -1.0,
    t_label: str = "NO_EVIDENCE",
    i_label: str = "NO_EVIDENCE"
) -> str:
    """
    Map trust_score (0-100) to one of:
    - APPROVE (>= 70)
    - HUMAN_REVIEW (40-69)
    - BLOCK (< 40)
    
    Override Rules: 
    1. If the record has a minor numeric deviation (<MINOR_DEVIATION_THRESHOLD), it must be at least HUMAN_REVIEW.
    2. If there is a genuine cross-modal conflict (one SUPPORT, one CONTRADICT), it must be at least HUMAN_REVIEW.
    """
    if trust_score >= 70.0:
        base_decision = "APPROVE"
    elif trust_score >= 40.0:
        base_decision = "HUMAN_REVIEW"
    else:
        base_decision = "BLOCK"
        
    if base_decision == "BLOCK":
        # Rule 1: Minor numeric deviation override
        if numeric_deviation != -1.0 and numeric_deviation < MINOR_DEVIATION_THRESHOLD:
            return "HUMAN_REVIEW"
            
        # Rule 2: Cross-modal conflict override
        supports = any(l == "SUPPORT" for l in [t_label, i_label])
        contradicts = any(l == "CONTRADICT" for l in [t_label, i_label])
        if supports and contradicts:
            return "HUMAN_REVIEW"
            
    return base_decision

if __name__ == "__main__":
    # Unit tests for boundaries
    assert get_decision(39.9) == "BLOCK", "Failed < 40 boundary"
    assert get_decision(40.0) == "HUMAN_REVIEW", "Failed >= 40 boundary"
    assert get_decision(69.9) == "HUMAN_REVIEW", "Failed < 70 boundary"
    assert get_decision(70.0) == "APPROVE", "Failed >= 70 boundary"
    
    # Override tests
    assert get_decision(10.0, numeric_deviation=0.08) == "HUMAN_REVIEW", "Failed minor deviation override"
    assert get_decision(10.0, numeric_deviation=0.30) == "BLOCK", "Failed major deviation bypass"
    
    assert get_decision(10.0, t_label="SUPPORT", i_label="CONTRADICT") == "HUMAN_REVIEW", "Failed cross-modal override"
    assert get_decision(10.0, t_label="CONTRADICT", i_label="CONTRADICT") == "BLOCK", "Failed unanimous contradict bypass"
    
    print("All decision boundary unit tests passed!")
