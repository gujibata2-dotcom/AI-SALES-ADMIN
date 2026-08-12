"""Observed capability discovery; candidates require repeated evidence and review."""

def discover(observations: list[dict], minimum_runs: int = 5) -> dict:
    if len(observations) < minimum_runs:
        return {"status": "OBSERVATION_ONLY", "candidate": None}
    capabilities = sorted({c for o in observations for c in o.get("capabilities", [])})
    return {"status": "CANDIDATE_CAPABILITY", "capabilities": capabilities, "requires_validation": True, "requires_governance": True}
