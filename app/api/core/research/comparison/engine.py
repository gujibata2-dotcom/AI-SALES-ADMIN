from typing import Iterable, Dict, Any
from ..models import Evidence

def compare_claims(claim_a: str, claim_b: str, context_a: Dict[str, Any], context_b: Dict[str, Any]) -> str:
    if claim_a == claim_b:
        return "AGREEMENT"
    for key, label in (("time", "TIME_DIFFERENCE"), ("definition", "DEFINITION_DIFFERENCE"), ("methodology", "METHODOLOGY_DIFFERENCE")):
        if context_a.get(key) != context_b.get(key) and key in context_a and key in context_b:
            return label
    if context_a.get("scope") != context_b.get("scope"):
        return "CONTEXT_DIFFERENCE"
    return "DIRECT_CONTRADICTION"

def resolve_conflict(classification: str, inspected: bool = False) -> str:
    if classification == "DIRECT_CONTRADICTION" and not inspected:
        return "UNRESOLVED"
    return "RESOLVED" if classification != "UNRESOLVED" else "UNRESOLVED"
