"""Decision record distinguishes facts, inferences, assumptions and recommendations."""
TYPES = ("FACT", "INFERENCE", "ASSUMPTION", "RECOMMENDATION")
def decision_record(decision_id: str, decision: str, options: list[str], evidence: list[dict], authority: str, reversibility: str) -> dict:
    return {"decision_id": decision_id, "decision": decision, "options": options, "evidence": evidence, "authority": authority, "reversibility": reversibility, "status": "NOT_EVALUATED"}
