"""Evaluation runner contract. Execution provider is injected; no production calls."""

def run_benchmark(benchmark: dict, tasks: list[dict], executor) -> list[dict]:
    results = []
    for task in tasks:
        result = executor(task)
        results.append({"task_id": task["task_id"], "result": result, "benchmark_id": benchmark["benchmark_id"], "dataset_version": benchmark["dataset_version"]})
    return results


def require_same_conditions(benchmark: dict, other: dict) -> None:
    for key in ("dataset_version", "metrics", "evaluation_method"):
        if benchmark.get(key) != other.get(key):
            raise ValueError(f"comparison invalid: {key} differs")
