from typing import Iterable, Dict, Any
from ..models import Hypothesis

def update_hypothesis(h: Hypothesis, result: str, supporting: bool) -> Hypothesis:
    status = "SUPPORTED" if supporting and result == "SUPPORTED" else "REJECTED" if result == "REJECTED" else "INCONCLUSIVE"
    return Hypothesis(h.hypothesis_id, h.statement, h.rationale, h.supporting_evidence, h.contradicting_evidence, h.testable_prediction, h.confidence, status)

def test_design(h: Hypothesis) -> Dict[str, Any]:
    return {"hypothesis_id": h.hypothesis_id, "prediction": h.testable_prediction, "status": "TESTING" if h.testable_prediction else "UNTESTABLE"}
