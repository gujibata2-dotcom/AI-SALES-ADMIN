"""Strategy contracts: versioned, evidence-aware, approval-gated."""
from dataclasses import dataclass

@dataclass(frozen=True)
class StrategyPlan:
    strategy_id: str
    version: str
    context: dict
    evidence: list[dict]
    approval: str | None
    effective_date: str | None
    review_date: str | None

    def can_publish(self) -> bool:
        return bool(self.evidence) and bool(self.approval) and bool(self.effective_date)
