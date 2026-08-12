def combine(knowledge_ids: list[str], reason: str, assumptions: list[str]) -> dict:
    return {"source_knowledge": knowledge_ids, "combination_reason": reason, "assumptions": assumptions, "novelty_status": "UNKNOWN"}
