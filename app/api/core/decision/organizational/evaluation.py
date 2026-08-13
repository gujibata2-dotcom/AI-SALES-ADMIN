"""Phase 41 decision evaluation and authorization helpers.

These helpers produce recommendations and gates; they never execute actions.
"""
from typing import Any, Iterable, Mapping
from .contracts import AuthorizationLevel, DecisionOption, Reversibility, Uncertainty

HARD_CONSTRAINT = "HARD_CONSTRAINT"
SOFT_CONSTRAINT = "SOFT_CONSTRAINT"


def detect_conflicts(objectives: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    items = list(objectives)
    conflicts: list[dict[str, Any]] = []
    for i, left in enumerate(items):
        for right in items[i + 1:]:
            if left.get("conflicts_with") == right.get("id") or right.get("conflicts_with") == left.get("id"):
                conflicts.append({"left": left.get("id"), "right": right.get("id"), "tradeoff": "EXPLICIT_CONFLICT"})
    return conflicts


def validate_constraints(constraints: Iterable[Mapping[str, Any]], facts: Mapping[str, Any]) -> list[str]:
    violations: list[str] = []
    for item in constraints:
        if item.get("mode") != HARD_CONSTRAINT:
            continue
        predicate = item.get("predicate")
        if predicate and facts.get(predicate) is False:
            violations.append(str(item.get("id", "unknown")))
    return violations


def evaluate_option(option: DecisionOption, criteria: Mapping[str, Any]) -> dict[str, Any]:
    """Return only evidence-backed fields; no fabricated numeric score."""
    result: dict[str, Any] = {"option_id": option.option_id, "reversibility": option.reversibility.value}
    result["numeric_utility"] = None
    result["utility_status"] = "NOT_EVALUATED"
    if criteria.get("basis") and criteria.get("weights"):
        result["utility_status"] = "EVALUABLE"
    return result


def authorization_level(*, risk: str, impact: str, reversibility: Reversibility, policy_allows: bool) -> AuthorizationLevel:
    if not policy_allows:
        return AuthorizationLevel.PROHIBITED
    if risk == "CRITICAL" or impact == "CRITICAL":
        return AuthorizationLevel.EXECUTIVE_APPROVAL_REQUIRED
    if reversibility == Reversibility.IRREVERSIBLE or risk == "HIGH" or impact == "HIGH":
        return AuthorizationLevel.HUMAN_APPROVAL_REQUIRED
    return AuthorizationLevel.POLICY_ALLOWED


def authorize(level: AuthorizationLevel, approval: Mapping[str, Any] | None) -> bool:
    if level in {AuthorizationLevel.PROHIBITED, AuthorizationLevel.HUMAN_APPROVAL_REQUIRED, AuthorizationLevel.EXECUTIVE_APPROVAL_REQUIRED} and not approval:
        return False
    if approval and not approval.get("authorized"):
        return False
    return True


def require_uncertainty_for_high_impact(impact: str, uncertainty: Uncertainty) -> None:
    if impact in {"HIGH", "CRITICAL"} and uncertainty == Uncertainty.UNKNOWN:
        raise ValueError("BLOCK: high-impact decision requires uncertainty information")
