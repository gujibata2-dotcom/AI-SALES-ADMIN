from typing import Any, Dict

def classify_budget(budget: Dict[str, Any]) -> str:
    limit, spent = budget.get("limit"), budget.get("spent", 0)
    if limit is None: return "UNKNOWN"
    if spent > limit: return "BUDGET_EXCEEDED"
    if limit and spent / limit >= 0.8: return "BUDGET_WARNING"
    return "HEALTHY"

def investment_decision(proposal: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": "PENDING_APPROVAL", "proposal": proposal, "requires_authorization": True}
