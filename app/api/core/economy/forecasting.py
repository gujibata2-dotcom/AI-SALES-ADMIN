from typing import Any, Dict

def forecast(expected_cost=None, best_case=None, worst_case=None, confidence=None) -> Dict[str, Any]:
    return {"expected_cost": expected_cost, "best_case": best_case, "worst_case": worst_case, "confidence": confidence, "status": "NOT_PROVIDED" if expected_cost is None else "KNOWN"}

def scenario(name: str, assumptions: list[str], impact: Any = None, probability_if_known: Any = None, response_plan: str | None = None) -> Dict[str, Any]:
    return {"scenario": name, "assumptions": assumptions, "impact": impact, "probability_if_known": probability_if_known, "response_plan": response_plan}
