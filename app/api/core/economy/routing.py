from typing import Any, Dict

def choose_model(candidates):
    """Return evidence-ranked candidates without hard-coding a provider winner."""
    return sorted(candidates, key=lambda x: (x.get("benchmark", 0), x.get("reliability", 0)), reverse=True)

def route_with_escalation(primary: Dict[str, Any], backup: Dict[str, Any], confidence: float, risk: str) -> Dict[str, Any]:
    if confidence < primary.get("min_confidence", 0) or risk in {"HIGH", "CRITICAL"}:
        return {"selected": backup.get("model_id"), "reason": "ESCALATE"}
    return {"selected": primary.get("model_id"), "reason": "PRIMARY"}
