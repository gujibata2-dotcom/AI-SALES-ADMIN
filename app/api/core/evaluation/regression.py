"""Regression detection against a prior evaluated version."""

METRICS = ("accuracy", "quality", "reliability", "safety")


def detect(previous: dict, current: dict, tolerance: float = 0.0) -> dict:
    drops = {m: previous[m] - current[m] for m in METRICS if m in previous and m in current and current[m] < previous[m] - tolerance}
    return {"status": "REGRESSION_ALERT" if drops else "NO_REGRESSION", "drops": drops}
