"""Phase 38 scientific reasoning core: evidence-first, falsifiable, reproducible workflows."""
from dataclasses import dataclass, field
from typing import Any

OBSERVATION_STATUS = {"RAW","VALIDATED","QUESTIONABLE","CONFLICTED","REJECTED","UNKNOWN"}
HYPOTHESIS_STATUS = {"PROPOSED","TESTABLE","TESTING","SUPPORTED","WEAKLY_SUPPORTED","CONTESTED","FALSIFIED","INCONCLUSIVE"}
EXPERIMENT_STATUS = {"DESIGNED","APPROVED","RUNNING","COMPLETED","FAILED","INVALID","REPLICATED","INCONCLUSIVE"}

@dataclass
class Observation:
    observation_id: str
    description: str
    source: str
    timestamp: str
    context: dict[str, Any] = field(default_factory=dict)
    measurement: Any = None
    uncertainty: Any = None
    status: str = "RAW"

@dataclass
class Measurement:
    measurement_id: str
    variable: str
    value: Any
    unit: str
    method: str
    source: str
    instrument_if_known: str | None = None
    precision: Any = None
    uncertainty: Any = None
    timestamp: str | None = None

    def validate(self) -> None:
        if not self.source:
            raise ValueError("measurement requires a source")

@dataclass
class Hypothesis:
    hypothesis_id: str
    statement: str
    rationale: str
    variables: list[str]
    assumptions: list[str]
    testable_prediction: str | None = None
    supporting_evidence: list[str] = field(default_factory=list)
    contradicting_evidence: list[str] = field(default_factory=list)
    confidence: str = "INCONCLUSIVE"
    status: str = "PROPOSED"

    def testability(self) -> str:
        return "NOT_TESTABLE" if not self.testable_prediction else "TESTABLE"

@dataclass
class Experiment:
    experiment_id: str
    hypothesis: str
    objective: str
    variables: list[str]
    controls: list[str]
    method: str
    sample: Any
    procedure: list[str]
    prediction: str
    result: Any = None
    limitations: list[str] = field(default_factory=list)
    status: str = "DESIGNED"
    baseline: str | None = None
    stopping_rules: list[str] = field(default_factory=list)

@dataclass
class ScientificResult:
    result_id: str
    experiment_id: str
    observed: Any
    comparison: str
    interpretation: str
    conclusion_type: str = "UNKNOWN"
    uncertainty: dict[str, Any] = field(default_factory=dict)

@dataclass
class Replication:
    replication_id: str
    original_experiment_id: str
    independent: bool
    result: Any
    status: str = "INCONCLUSIVE"

class ScienceEngine:
    LIFECYCLE = ["OBSERVE","MEASURE","QUESTION","MODEL","HYPOTHESIZE","PREDICT","EXPERIMENT","OBSERVE_RESULTS","COMPARE","FALSIFY_SUPPORT","UPDATE_BELIEF","PEER_REVIEW","HUMAN_REVIEW_IF_REQUIRED","PUBLISH_KNOWLEDGE","LEARN"]

    def falsification_test(self, hypothesis: Hypothesis) -> dict[str, str]:
        return {"question": "What evidence would prove this hypothesis wrong?", "falsification_test": hypothesis.testable_prediction or "UNKNOWN", "status": hypothesis.testability()}

    def validate_result(self, result: ScientificResult, has_data: bool, replicated: bool = False) -> str:
        if not has_data: return "UNKNOWN"
        if replicated: return "SUPPORTED_BY_EVIDENCE"
        return result.conclusion_type if result.conclusion_type in {"SUPPORTED_BY_EVIDENCE","INFERENCE","SPECULATION","UNKNOWN"} else "UNKNOWN"

    def authorize(self, environment: str, risk: str, approval: str | None) -> bool:
        if environment == "PRODUCTION" or risk in {"HIGH","CRITICAL","REGULATED"}:
            return approval == "APPROVED"
        return approval in {"APPROVED","NOT_REQUIRED"}

    def simulation_label(self) -> str:
        return "SIMULATED"
