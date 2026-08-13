"""Adaptive strategy and outcome contracts for Phase 41."""
from dataclasses import dataclass, field
from typing import Any, Mapping
from .contracts import StrategyStatus

@dataclass
class StrategyRecord:
    strategy_id: str
    objective: list[str]
    assumptions: list[str]
    initiatives: list[str]
    risks: list[str]
    scenarios: list[str]
    metrics: list[str]
    decision_rules: list[str]
    version: int = 1
    status: StrategyStatus = StrategyStatus.DRAFT
    history: list[Mapping[str, Any]] = field(default_factory=list)

@dataclass(frozen=True)
class OutcomeRecord:
    outcome_id: str
    decision_id: str
    expected: Mapping[str, Any]
    actual: Mapping[str, Any]
    timestamp: str
    deviation: Mapping[str, Any]
    evidence: tuple[str, ...] = ()
    impact: Mapping[str, Any] | None = None

class StrategyRegistry:
    def __init__(self) -> None:
        self._current: dict[str, StrategyRecord] = {}
        self._history: dict[str, list[StrategyRecord]] = {}

    def register(self, strategy: StrategyRecord) -> None:
        self._current[strategy.strategy_id] = strategy
        self._history.setdefault(strategy.strategy_id, []).append(strategy)

    def adapt(self, strategy_id: str, *, trigger: str, reason: str, evidence_refs: list[str]) -> StrategyRecord:
        current = self._current[strategy_id]
        if not evidence_refs:
            raise ValueError("adaptation requires evidence references")
        updated = StrategyRecord(
            strategy_id=current.strategy_id,
            objective=current.objective,
            assumptions=current.assumptions,
            initiatives=current.initiatives,
            risks=current.risks,
            scenarios=current.scenarios,
            metrics=current.metrics,
            decision_rules=current.decision_rules,
            version=current.version + 1,
            status=StrategyStatus.ADAPTING,
            history=current.history + [{"trigger": trigger, "reason": reason, "evidence": evidence_refs, "from_version": current.version}],
        )
        self.register(updated)
        return updated

    def history(self, strategy_id: str) -> tuple[StrategyRecord, ...]:
        return tuple(self._history.get(strategy_id, ()))


def strategy_drift(baseline: Mapping[str, Any], reality: Mapping[str, Any]) -> dict[str, Any]:
    """Only report observable drift; no invented score."""
    changed = sorted(k for k in baseline.keys() & reality.keys() if baseline[k] != reality[k])
    return {"changed_factors": changed, "strategy_drift_score": None if not changed else "UNKNOWN", "status": "UNKNOWN" if changed else "NO_OBSERVED_DRIFT"}


def decision_quality(*, evidence_sufficient: bool, assumptions_reasonable: bool, risks_identified: bool, authorization_correct: bool, outcome_good: bool) -> str:
    if not evidence_sufficient:
        return "INSUFFICIENT_EVIDENCE"
    decision_good = all((assumptions_reasonable, risks_identified, authorization_correct))
    if decision_good and outcome_good: return "GOOD_DECISION_GOOD_OUTCOME"
    if decision_good: return "GOOD_DECISION_BAD_OUTCOME"
    if outcome_good: return "BAD_DECISION_GOOD_OUTCOME"
    return "BAD_DECISION_BAD_OUTCOME"
