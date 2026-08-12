def phase36_to_opportunity(finding_id: str, problem: str) -> dict:
    return {"source": "PHASE_36", "finding_id": finding_id, "problem": problem, "opportunity_status": "DISCOVERED"}

def phase35_to_opportunity(capability_gap: str, cost: str) -> dict:
    return {"source": "PHASE_35", "capability_gap": capability_gap, "cost": cost, "opportunity_status": "DISCOVERED"}

def phase12_feedback_to_problem(feedback_ids: list[str]) -> dict:
    return {"source": "PHASE_12", "feedback_ids": feedback_ids, "problem_status": "DISCOVERED"}

def workforce_assignment(role: str, subject_id: str) -> dict:
    return {"phase": "PHASE_33", "role": role, "subject_id": subject_id}

def governance_gate(risk: str, approval: str | None) -> bool:
    return risk not in {"HIGH", "CRITICAL", "REGULATED"} or approval == "APPROVED"
