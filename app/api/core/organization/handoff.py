"""Standardized cross-employee handoff contract."""
REQUIRED = ("context", "objective", "work_completed", "evidence", "open_questions", "risks", "next_action")

def validate(handoff: dict) -> bool:
    missing = [k for k in REQUIRED if k not in handoff]
    if missing: raise ValueError(f"Invalid handoff: {missing}")
    return True
