"""Phase 33 workforce orchestration contracts."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class WorkforceStatus(str, Enum):
    AVAILABLE='AVAILABLE'; BUSY='BUSY'; TRAINING='TRAINING'; REVIEW='REVIEW'; PAUSED='PAUSED'; SUSPENDED='SUSPENDED'; OFFLINE='OFFLINE'; RETIRED='RETIRED'

class TeamType(str, Enum):
    SINGLE_AGENT='SINGLE_AGENT'; SPECIALIST_PAIR='SPECIALIST_PAIR'; CROSS_FUNCTIONAL='CROSS_FUNCTIONAL'; REVIEW_TEAM='REVIEW_TEAM'; RESEARCH_TEAM='RESEARCH_TEAM'; ENGINEERING_TEAM='ENGINEERING_TEAM'; SALES_TEAM='SALES_TEAM'; SUPPORT_TEAM='SUPPORT_TEAM'; SECURITY_TEAM='SECURITY_TEAM'; EMERGENCY_TEAM='EMERGENCY_TEAM'; CUSTOM='CUSTOM'

@dataclass(frozen=True)
class WorkforceMember:
    employee_id: str
    role: str
    capabilities: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
    availability: WorkforceStatus = WorkforceStatus.AVAILABLE
    workload: float = 0.0
    reliability: float | None = None
    cost: float | None = None

@dataclass(frozen=True)
class TeamRecommendation:
    mode: str
    reason: str
    required_capabilities: tuple[str, ...] = ()
    risk_level: str = 'LOW'

@dataclass
class WorkforceEvent:
    workforce_event_id: str
    task_id: str
    action: str
    reason: str
    evidence: list[str] = field(default_factory=list)
    permission: str | None = None
    result: str | None = None

def choose_execution_mode(*, complexity:int, risk:str, required_capabilities:int, cost_single:float=1.0, cost_team:float=2.0) -> TeamRecommendation:
    if complexity <= 2 and risk == 'LOW' and required_capabilities <= 1:
        return TeamRecommendation('SINGLE_AGENT','simple low-risk task')
    return TeamRecommendation('MULTI_AGENT','complexity, risk, or capability coverage requires collaboration', risk_level=risk)

def eligible(member: WorkforceMember, required_capabilities:set[str], required_permissions:set[str]) -> bool:
    return (member.availability == WorkforceStatus.AVAILABLE and member.workload < 1.0
            and required_capabilities.issubset(set(member.capabilities))
            and required_permissions.issubset(set(member.permissions)))
