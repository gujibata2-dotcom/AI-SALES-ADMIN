from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class ModelEconomics:
    model_id: str
    capability_evidence: Dict[str, Any] = field(default_factory=dict)
    cost: Optional[float] = None
    latency: Optional[float] = None
    reliability: Optional[float] = None
    status: str = "NOT_EVALUATED"

@dataclass(frozen=True)
class ToolEconomics:
    tool_id: str
    capability_evidence: Dict[str, Any] = field(default_factory=dict)
    cost: Optional[float] = None
    success_rate: Optional[float] = None
    failure_rate: Optional[float] = None
    security_status: str = "UNKNOWN"

@dataclass(frozen=True)
class InvestmentProposal:
    investment_id: str
    target: str
    expected_benefit: Optional[float]
    cost: Optional[float]
    risk: Optional[str]
    timeline: Optional[str]
    confidence: Optional[float]
    approval: Optional[str] = None
    status: str = "PENDING_APPROVAL"
