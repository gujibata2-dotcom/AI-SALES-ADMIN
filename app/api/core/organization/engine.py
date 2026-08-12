from dataclasses import dataclass
from typing import Any

AUTHORITY = ("AI_AUTONOMOUS", "AI_WITH_REVIEW", "HUMAN_APPROVAL", "HUMAN_ONLY")
RISK_LEVELS = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
EVIDENCE_KINDS = ("FACT", "INFERENCE", "ASSUMPTION", "RECOMMENDATION")

@dataclass(frozen=True)
class StrategicAction:
    organization_id: str
    action: str
    authority: str
    reversible: str
    evidence: list[dict[str, Any]]
    approval: str | None = None

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.authority not in AUTHORITY: errors.append("invalid authority")
        if self.reversible not in ("REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE"): errors.append("invalid reversibility")
        if self.reversible == "IRREVERSIBLE" and self.authority not in ("HUMAN_APPROVAL", "HUMAN_ONLY"): errors.append("irreversible action requires human governance")
        if not self.evidence and self.authority != "HUMAN_ONLY": errors.append("evidence required")
        return errors


def classify_status(target: float | None, actual: float | None) -> str:
    if target is None or actual is None: return "NOT_EVALUATED"
    if actual >= target: return "ON_TRACK"
    if actual >= target * 0.8: return "AT_RISK"
    return "OFF_TRACK"
