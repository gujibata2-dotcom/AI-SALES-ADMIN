"""Auditable career event contract with evidence and approval references."""


def career_event(employee_id: str, event_type: str, previous_state: dict, new_state: dict,
                 evidence: list[str] | None = None, evaluator: str | None = None,
                 approval: str | None = None, reason: str | None = None) -> dict:
    return {"career_event_id": f"career:{employee_id}:{event_type}", "employee_id": employee_id,
            "event_type": event_type, "previous_state": previous_state, "new_state": new_state,
            "evidence": evidence or [], "evaluator": evaluator, "timestamp": "UNSET",
            "approval": approval, "reason": reason}
