"""Phase 41 safety helpers: recommendations are not decisions."""
from .contracts import AUTHORIZATION_LEVELS


def authorization_level(*, risk: str, impact: str, irreversible: bool, policy_allows: bool) -> str:
    if not policy_allows: return "PROHIBITED"
    if risk == "CRITICAL" or impact == "CRITICAL": return "EXECUTIVE_APPROVAL_REQUIRED"
    if irreversible or risk == "HIGH" or impact == "HIGH": return "HUMAN_APPROVAL_REQUIRED"
    return "POLICY_ALLOWED"


def decision_from_recommendation(recommendation: dict) -> dict:
    auth = recommendation.get("authorization") or {}
    if auth.get("status") != "AUTHORIZED" or not auth.get("authority_reference"):
        raise PermissionError("recommendation cannot become a decision without explicit authorization")
    return {**recommendation, "state": "AUTHORIZED"}


def execution_handoff(decision: dict) -> dict:
    if decision.get("state") != "AUTHORIZED":
        raise PermissionError("only authorized decisions may be handed to Phase 24")
    return {"execution_request_status": "READY_FOR_PHASE_24", "decision_id": decision["decision_id"]}
