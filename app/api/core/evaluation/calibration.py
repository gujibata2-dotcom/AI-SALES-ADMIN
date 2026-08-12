"""Confidence calibration without treating confidence as accuracy."""

def calibration_report(predictions: list[dict]) -> dict:
    if not predictions:
        return {"status": "NOT_EVALUATED"}
    bins = []
    for p in predictions:
        confidence = float(p.get("confidence", 0))
        actual = 1.0 if p.get("correct") else 0.0
        bins.append({"confidence": confidence, "accuracy": actual, "error": abs(confidence - actual)})
    mean_error = sum(x["error"] for x in bins) / len(bins)
    return {"status": "CALIBRATION_FAILURE" if mean_error > 0.2 else "CALIBRATED", "mean_absolute_calibration_error": mean_error, "samples": len(bins)}
