"""Resource allocation is recommendation-first and human-gated for high impact."""
def allocation_request(goal_id: str, resources: dict, impact: str = "LOW") -> dict:
    return {"goal_id": goal_id, "resources": resources, "impact": impact, "status": "PENDING_REVIEW" if impact in ("HIGH", "CRITICAL") else "RECOMMENDATION"}
