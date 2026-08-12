"""Governance policy precedence and human-owner boundaries."""

def resolve_policy_conflict(policies: list[dict]) -> dict:
    if not policies: return {"status": "NOT_EVALUATED"}
    ranked = sorted(policies, key=lambda p: p.get("authority_rank", 0), reverse=True)
    if len(ranked) > 1 and ranked[0].get("authority_rank") == ranked[1].get("authority_rank"):
        return {"status": "ESCALATE", "reason": "ambiguous policy authority"}
    return {"status": "RESOLVED", "policy_id": ranked[0].get("policy_id")}
