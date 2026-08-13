"""Causal reasoning deliberately separates correlation from causation."""

def classify_claim(kind: str) -> str:
    allowed={"CAUSE","EFFECT","CORRELATION","CONFOUNDING","MEDIATION","MODERATION"}
    return kind if kind in allowed else "UNKNOWN"

def causal_graph(nodes: list[str], edges: list[tuple[str,str]]) -> dict:
    node_set=set(nodes)
    valid=[e for e in edges if len(e)==2 and e[0] in node_set and e[1] in node_set]
    return {"nodes":nodes,"edges":valid,"status":"UNVERIFIED"}

def avoid_causation_overclaim(correlation_value, causal_evidence: bool) -> str:
    if not causal_evidence: return "CORRELATION_ONLY"
    return "CAUSAL_CLAIM_SUPPORTED" if correlation_value is not None else "UNKNOWN"
