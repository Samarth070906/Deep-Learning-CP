import re

def extract_number_with_unit(text: str, unit: str):
    if not text:
        return None
    if unit:
        # Match number right before the unit
        pattern = r"(\d+(?:\.\d+)?)\s*" + re.escape(unit)
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return float(matches[-1])
        return None
    else:
        # If no unit provided, assume categorical/non-numeric unless we explicitly want a fallback.
        # It's safer to just return None (non-numeric) if there is no unit,
        # but let's fall back to last number if it seems to be a pure numeric attribute.
        # Actually, if there is no unit, it's safer to NOT extract blind digits to avoid sentinel collision.
        return None

def get_numeric_deviation(claim_text: str, evidence_text: str, unit: str = None):
    """
    Extracts the numeric deviation between claim and evidence texts using unit anchors.
    Returns deviation_pct or -1.0 if not parseable or not numeric.
    """
    if not unit:
        return -1.0
        
    val_claim = extract_number_with_unit(claim_text, unit)
    val_evidence = extract_number_with_unit(evidence_text, unit)
    
    if val_claim is None or val_evidence is None:
        return -1.0
        
    if val_evidence == 0:
        if val_claim == 0:
            return 0.0
        return 1.0
        
    deviation_pct = abs(val_claim - val_evidence) / val_evidence
    return min(deviation_pct, 1.0)
