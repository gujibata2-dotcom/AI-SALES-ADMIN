"""Phase 41 organizational decision and adaptive strategy contracts."""

DECISION_STATES = ("RECOMMENDATION", "AUTHORIZED", "EXECUTING", "COMPLETED", "REJECTED", "UNKNOWN")
EVIDENCE_STATES = ("KNOWN", "ESTIMATED", "UNCERTAIN", "CONTESTED", "UNKNOWN")
AUTHORIZATION_LEVELS = ("AUTO_ALLOWED", "POLICY_ALLOWED", "HUMAN_APPROVAL_REQUIRED", "EXECUTIVE_APPROVAL_REQUIRED", "PROHIBITED")
REVERSIBILITY = ("REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE")


def require_authorization(recommendation: dict) -> bool:
    """Return whether a recommendation has an explicit authorization contract."""
    authorization = recommendation.get("authorization") or {}
    return bool(authorization.get("status") == "AUTHORIZED" and authorization.get("authority_reference"))


def decision_quality_class(*, evidence_sufficient: bool, decision_sound: bool, outcome_good: bool) -> str:
    if not evidence_sufficient:
        return "INSUFFICIENT_EVIDENCE"
    if decision_sound and outcome_good:
        return "GOOD_DECISION_GOOD_OUTCOME"
    if decision_sound and not outcome_good:
        return "GOOD_DECISION_BAD_OUTCOME"
    if not decision_sound and outcome_good:
        return "BAD_DECISION_GOOD_OUTCOME"
    return "BAD_DECISION_BAD_OUTCOME"


def uncertainty_state(value: str) -> str:
    if value not in EVIDENCE_STATES:
        raise ValueError(f"unsupported uncertainty state: {value}")
    return value
