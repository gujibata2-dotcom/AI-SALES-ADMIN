def compare_baseline(baseline: dict, candidate: dict, metrics: list[str]) -> dict:
    return {m: {"baseline": baseline.get(m, "UNKNOWN"), "candidate": candidate.get(m, "UNKNOWN"), "status": "MEASURED" if m in baseline and m in candidate else "UNKNOWN"} for m in metrics}
