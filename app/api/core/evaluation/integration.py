"""Bounded integration contracts for Phase 26 model routing and Phase 30 organization.

Evaluation evidence can inform routing and employee selection; it cannot grant permissions or bypass governance.
"""

def routing_evidence(capability_score: dict) -> dict:
    return {"employee_id": capability_score.get("employee_id"), "capability": capability_score.get("capability"), "status": capability_score.get("status"), "evidence_references": capability_score.get("evidence_references", [])}


def eligible_for_task(profile: dict, required_capability: str, required_permission: str) -> bool:
    return (required_capability in profile.get("capabilities", []) and required_permission in profile.get("permissions", []) and profile.get("status") == "ACTIVE")
