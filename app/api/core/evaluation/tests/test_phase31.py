"""Synthetic Phase 31 contract tests; no production data or external calls."""
from app.api.core.evaluation.calibration import calibration_report
from app.api.core.evaluation.engine import compare, component_scores
from app.api.core.evaluation.promotion import recommend
from app.api.core.evaluation.regression import detect


def test_not_evaluated_without_human_baseline():
    assert compare({"accuracy": 1}, {"status": "NOT_EVALUATED"})["status"] == "INCONCLUSIVE"


def test_component_scores_are_traceable():
    assert component_scores({"accuracy": 0.9})["accuracy_score"] == 0.9
    assert component_scores({"accuracy": 0.9})["quality_score"] is None


def test_calibration_failure():
    r = calibration_report([{"confidence": 0.99, "correct": False}] * 3)
    assert r["status"] == "CALIBRATION_FAILURE"


def test_superhuman_requires_review():
    r = recommend("EXPERT", {"evaluation_ids": ["e1"], "sample_size": 100, "reliability": 0.99, "safety": 0.99, "result": "PASS", "limitations": []}, "SUPERHUMAN_SPECIALIST")
    assert r["status"] == "HUMAN_REVIEW_REQUIRED"


def test_regression_alert():
    assert detect({"accuracy": 0.9, "quality": 0.9, "reliability": 0.9, "safety": 0.9}, {"accuracy": 0.8, "quality": 0.9, "reliability": 0.9, "safety": 0.9})["status"] == "REGRESSION_ALERT"
