"""Simulation and what-if outputs are explicitly labeled as scenarios."""

def run_scenario(name: str, parameters: dict, assumptions: list[str], iterations: int) -> dict:
    return {"scenario":name,"parameters":parameters,"assumptions":assumptions,"iterations":iterations,"outputs":[],"uncertainty":{},"result_type":"SIMULATED"}

def what_if(question: str, changed_assumption: str) -> dict:
    return {"question":question,"changed_assumption":changed_assumption,"type":"COUNTERFACTUAL","status":"SCENARIO"}
