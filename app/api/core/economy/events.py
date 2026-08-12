from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class EconomicEvent:
    economy_event_id: str
    actor: str
    action: str
    resource_id: Optional[str]
    task_id: Optional[str]
    cost: Optional[float]
    value: Optional[float]
    decision: str
    reason: str
    evidence: Dict[str, Any]
    approval: Optional[str]
    timestamp: str
    outcome: Optional[str] = None
