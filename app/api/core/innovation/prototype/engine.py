def iterate(prototype_id: str, current_version: str, failure_evidence: list[str]) -> dict:
    return {"prototype_id":prototype_id,"previous_version":current_version,"next_version":f"{current_version}.next","failure_evidence":failure_evidence}
