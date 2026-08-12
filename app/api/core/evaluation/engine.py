"""Provider-neutral benchmark and scoring contracts. No fabricated results."""
from dataclasses import dataclass, field
from statistics import mean, median, variance

@dataclass(frozen=True)
class BenchmarkRun:
    evaluation_id: str
    employee_id: str
    benchmark_id: str
    model_id: str
    model_version: str
    dataset_version: str
    metrics: dict[str, float]
    passed: bool | None = None
    confidence: float | None = None

@dataclass
class Aggregate:
    runs: list[BenchmarkRun] = field(default_factory=list)

    def summary(self, metric: str) -> dict:
        values = [r.metrics[metric] for r in self.runs if metric in r.metrics]
        if not values:
            return {"status": "NOT_EVALUATED"}
        return {"status": "EVALUATED", "runs": len(values), "mean": mean(values), "median": median(values), "variance": variance(values) if len(values) > 1 else 0.0, "best": max(values), "worst": min(values)}


def component_scores(metrics: dict[str, float]) -> dict[str, float | None]:
    names = ("accuracy", "quality", "reliability", "reasoning", "speed", "safety", "tool_use", "adaptability", "learning", "cost_efficiency")
    return {f"{n}_score": metrics.get(n) for n in names}


def compare(ai: dict, human: dict) -> dict:
    if human.get("status") != "EVALUATED":
        return {"status": "INCONCLUSIVE", "reason": "human baseline unavailable"}
    keys = ("accuracy", "quality", "completion_time", "error_rate", "reliability")
    return {k: {"ai": ai.get(k), "human": human.get(k), "delta": (ai.get(k) - human.get(k)) if isinstance(ai.get(k), (int,float)) and isinstance(human.get(k), (int,float)) else None} for k in keys}
