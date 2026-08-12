"""Specialization discovery requires repeated verified evidence."""


def discover_candidate(employee_id: str, domain: str, evidence: list[dict], minimum_sample: int = 5) -> dict:
    verified = [e for e in evidence if e.get("verified") is True and e.get("domain") == domain]
    if len(verified) < minimum_sample:
        return {"employee_id": employee_id, "domain": domain, "status": "NOT_EVALUATED", "evidence_count": len(verified)}
    return {"employee_id": employee_id, "domain": domain, "status": "CANDIDATE",
            "evidence_count": len(verified), "reliability": min(e.get("reliability", 0) for e in verified),
            "requires_governance_review": True}
