from trustagent.pipeline.decision import MINOR_DEVIATION_THRESHOLD

def generate_explanation(
    claim_text: str,
    t_label: str,
    t_score: float,
    i_label: str,
    i_score: float,
    numeric_deviation: float,
    consistency_score: float,
    trust_score: float,
    decision: str
) -> str:
    lines = []
    lines.append(f"Claim: '{claim_text}'")
    
    # Evidence Checked
    mods = []
    if t_label != "NO_EVIDENCE":
        mods.append("Text")
    if i_label != "NO_EVIDENCE":
        mods.append("Image")
        
    if not mods:
        lines.append("Evidence Checked: None (Neither Text nor Image provided valid evidence).")
    else:
        lines.append(f"Evidence Checked: {' and '.join(mods)}.")
        if t_label == "NO_EVIDENCE":
            lines.append(" - Note: Text evidence was checked but yielded NO EVIDENCE.")
        if i_label == "NO_EVIDENCE":
            lines.append(" - Note: Image evidence was checked but yielded NO EVIDENCE.")
            
    # Agreement / Disagreement & Deviation
    if not mods:
        lines.append("Result: Cannot verify due to lack of evidence.")
    else:
        supports = any(l == "SUPPORT" for l in [t_label, i_label])
        contradicts = any(l == "CONTRADICT" for l in [t_label, i_label])
        
        is_mixed = supports and contradicts
        
        if supports and not contradicts:
            lines.append("Result: Evidence AGREES with the claim.")
        elif contradicts and not supports:
            lines.append("Result: Evidence DISAGREES with the claim.")
        else:
            lines.append("Result: Mixed evidence (some support, some contradiction).")
            
        # Numeric Deviation Details
        if numeric_deviation != -1.0:
            dev_pct = numeric_deviation * 100.0
            if dev_pct == 0.0:
                lines.append(f" - The numeric values match exactly (0% deviation).")
            else:
                lines.append(f" - The evidence differs numerically by {dev_pct:.1f}%.")
                if decision != "APPROVE" and numeric_deviation < MINOR_DEVIATION_THRESHOLD:
                    lines.append("   (Note: Review this deviation manually, as the strict model may heavily penalize minor numeric differences).")
        else:
            if is_mixed:
                lines.append(" - The attribute is categorical or non-numeric, and the evidence conflicts across modalities.")
            elif contradicts:
                lines.append(" - The attribute is categorical or non-numeric, and the evidence represents a direct contradiction.")
                
    # Final Score & Decision
    lines.append(f"Decision: {decision} (Trust Score: {trust_score:.1f}/100)")
    
    return "\n".join(lines)
