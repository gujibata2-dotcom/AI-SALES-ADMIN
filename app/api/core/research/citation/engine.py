from typing import Dict, Any

def citation(source_id: str, claim_id: str, location: str | None, retrieval_time: str | None) -> Dict[str, Any]:
    if not source_id or not claim_id:
        raise ValueError("citation requires source_id and claim_id")
    return {"source_id": source_id, "claim_id": claim_id, "location": location, "retrieval_time": retrieval_time}

def trace_claim(claim_id: str, evidence_by_claim: Dict[str, list[str]]) -> Dict[str, Any]:
    evidence = evidence_by_claim.get(claim_id, [])
    return {"claim_id": claim_id, "traceable": bool(evidence), "evidence_ids": evidence}
