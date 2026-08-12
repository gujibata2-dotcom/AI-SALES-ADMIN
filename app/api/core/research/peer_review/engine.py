from typing import Dict, Any

def review_gate(review: Dict[str, Any]) -> Dict[str, Any]:
    required = ["accuracy", "evidence", "logic", "source_quality", "missing_context", "contradictions", "uncertainty", "citation"]
    missing = [k for k in required if not review.get(k)]
    if missing:
        return {"decision": "INCONCLUSIVE", "missing": missing}
    return {"decision": review.get("decision", "INCONCLUSIVE"), "missing": []}

def blind_review_policy(critical: bool, independent: bool) -> Dict[str, Any]:
    return {"required": critical, "independent": independent, "hide_prior_conclusion": bool(critical and independent)}
