"""Phase 41 organizational decision contracts integrated with the existing decision engine.

Pure standard-library contracts. No provider, network, or execution dependency.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

class EvidenceClass(str, Enum):
    FACT="FACT"; EVIDENCE="EVIDENCE"; INFERENCE="INFERENCE"; ASSUMPTION="ASSUMPTION"; PREDICTION="PREDICTION"
class Uncertainty(str, Enum):
    KNOWN="KNOWN"; ESTIMATED="ESTIMATED"; UNCERTAIN="UNCERTAIN"; CONTESTED="CONTESTED"; UNKNOWN="UNKNOWN"
class Reversibility(str, Enum):
    REVERSIBLE="REVERSIBLE"; PARTIALLY_REVERSIBLE="PARTIALLY_REVERSIBLE"; IRREVERSIBLE="IRREVERSIBLE"
class AuthorizationLevel(str, Enum):
    AUTO_ALLOWED="AUTO_ALLOWED"; POLICY_ALLOWED="POLICY_ALLOWED"; HUMAN_APPROVAL_REQUIRED="HUMAN_APPROVAL_REQUIRED"; EXECUTIVE_APPROVAL_REQUIRED="EXECUTIVE_APPROVAL_REQUIRED"; PROHIBITED="PROHIBITED"
class StrategyStatus(str, Enum):
    DRAFT="DRAFT"; PROPOSED="PROPOSED"; REVIEW="REVIEW"; APPROVED="APPROVED"; ACTIVE="ACTIVE"; PAUSED="PAUSED"; ADAPTING="ADAPTING"; SUPERSEDED="SUPERSEDED"; RETIRED="RETIRED"

@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    classification: EvidenceClass
    source_reference: str
    verified: bool = False
    provenance: tuple[str, ...] = ()

@dataclass(frozen=True)
class Constraint:
    constraint_id: str
    kind: str
    mode: str
    description: str

@dataclass(frozen=True)
class DecisionOption:
    option_id: str
    title: str
    rationale: str = ""
    evidence_refs: tuple[str, ...] = ()
    reversibility: Reversibility = Reversibility.REVERSIBLE

@dataclass
class DecisionRecord:
    decision_id: str
    title: str
    context: Mapping[str, Any]
    objectives: list[str]
    constraints: list[Constraint]
    evidence: list[EvidenceRef]
    options: list[DecisionOption]
    selected_option: str | None = None
    assumptions: list[str] = field(default_factory=list)
    risks: list[Mapping[str, Any]] = field(default_factory=list)
    uncertainty: Uncertainty = Uncertainty.UNKNOWN
    authorization: Mapping[str, Any] | None = None
    expected_outcome: Mapping[str, Any] | None = None
    actual_outcome: Mapping[str, Any] | None = None
    decision_quality: str | None = None
    version: int = 1

class DecisionRegistry:
    """Append-only historical registry for decision state; execution remains outside this module."""
    def __init__(self) -> None:
        self._current: dict[str, DecisionRecord] = {}
        self._history: dict[str, list[DecisionRecord]] = {}

    def register(self, record: DecisionRecord) -> None:
        if record.selected_option and record.selected_option not in {o.option_id for o in record.options}:
            raise ValueError("selected option must exist")
        if record.selected_option and not record.authorization:
            raise PermissionError("BLOCK: authorization required before decision selection")
        self._current[record.decision_id] = record
        self._history.setdefault(record.decision_id, []).append(record)

    def get(self, decision_id: str) -> DecisionRecord | None:
        return self._current.get(decision_id)

    def history(self, decision_id: str) -> tuple[DecisionRecord, ...]:
        return tuple(self._history.get(decision_id, ()))

def classify_information(has_source: bool, verified: bool, inferential: bool = False) -> EvidenceClass:
    if not has_source: return EvidenceClass.ASSUMPTION
    if inferential: return EvidenceClass.INFERENCE
    return EvidenceClass.FACT if verified else EvidenceClass.EVIDENCE

def numeric_utility_allowed(criteria: Mapping[str, Any]) -> bool:
    return bool(criteria.get("basis") and criteria.get("weights"))

def preserve_external_content_as_data(content: Any) -> dict[str, Any]:
    return {"data": content, "instructions_trusted": False}
