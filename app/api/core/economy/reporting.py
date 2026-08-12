from typing import Any, Dict

def report(budget: Dict[str, Any], utilization: Dict[str, Any], value: Dict[str, Any], risk: Any = None) -> Dict[str, Any]:
    return {"budget": budget, "resource_utilization": utilization, "value": value, "risk": risk, "status": "NOT_EVALUATED" if not value else "REPORT"}
