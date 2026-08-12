"""Risk escalation contracts. AI cannot lower risk merely to pass governance."""
LEVELS = ("LOW", "MEDIUM", "HIGH", "CRITICAL")

def required_authority(level: str) -> str:
    if level == "CRITICAL": return "HUMAN_ONLY"
    if level == "HIGH": return "HUMAN_APPROVAL"
    if level == "MEDIUM": return "AI_WITH_REVIEW"
    return "AI_AUTONOMOUS"

def assess(*, impact: float, likelihood: float, detectability: float, reversibility: float) -> dict:
    return {"impact": impact, "likelihood": likelihood, "detectability": detectability, "reversibility": reversibility, "status": "NOT_EVALUATED"}
