"""Continuous mastery state; MASTERED is never terminal."""

MASTERY_REQUIREMENTS = {
    "MASTERED": ("repeated_evidence", "high_reliability", "high_difficulty", "stable_performance", "low_regression")
}


def assess_mastery(evidence: dict) -> str:
    if evidence.get("status") == "NOT_EVALUATED":
        return "NOT_EVALUATED"
    if all(evidence.get(k) is True for k in MASTERY_REQUIREMENTS["MASTERED"]):
        return "MASTERED"
    return evidence.get("level", "DEVELOPING")


def maintenance_due(last_evaluated_at: str | None, challenge_available: bool) -> bool:
    return bool(challenge_available and last_evaluated_at)
