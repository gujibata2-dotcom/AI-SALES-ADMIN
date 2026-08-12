from typing import Any, Dict, Iterable, Optional

UNKNOWN = "UNKNOWN"
NOT_PROVIDED = "NOT_PROVIDED"

class EconomyEngine:
    """Pure decision helpers; no payment, purchase, transfer, or self-approval side effects."""
    def allocation_recommendation(self, goal: Dict[str, Any], resources: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        return {"status": "RECOMMENDATION", "goal_id": goal.get("goal_id"), "resources": list(resources), "requires_approval": True}

    def cost_status(self, amount: Optional[float], provider_disclosed: bool) -> str:
        if amount is None or not provider_disclosed:
            return "COST_UNKNOWN"
        return "KNOWN"

    def roi(self, verified_benefit: Optional[float], investment_cost: Optional[float]) -> Dict[str, Any]:
        if verified_benefit is None or investment_cost is None or investment_cost <= 0:
            return {"status": "ROI_UNDETERMINED", "roi": None}
        return {"status": "DETERMINED", "roi": (verified_benefit - investment_cost) / investment_cost}

    def capacity_gap(self, required: Optional[float], available: Optional[float]) -> Dict[str, Any]:
        if required is None or available is None:
            return {"status": UNKNOWN, "gap": None}
        gap = max(required - available, 0)
        return {"status": "CAPACITY_GAP" if gap else "SUFFICIENT", "gap": gap}

    def authorize_financial_action(self, approval: Optional[str], action: str) -> Dict[str, Any]:
        if action in {"TRANSFER", "PURCHASE", "CONTRACT", "INCREASE_BUDGET", "CREATE_OBLIGATION"} and not approval:
            return {"allowed": False, "reason": "HUMAN_OR_AUTHORIZED_APPROVAL_REQUIRED"}
        return {"allowed": True, "reason": "POLICY_CHECK_PASSED"}
