SCENARIOS = ("BASELINE", "OPTIMISTIC", "PESSIMISTIC", "ADVERSE", "UNKNOWN")
def scenario(name: str, assumptions: list[str], impact: str, probability_if_known: float | None = None) -> dict:
    if name not in SCENARIOS: raise ValueError("invalid scenario")
    return {"name": name, "assumptions": assumptions, "impact": impact, "probability_if_known": probability_if_known}
