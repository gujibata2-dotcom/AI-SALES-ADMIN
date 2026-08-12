from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

class RiskLevel(str, Enum):
    READ_ONLY="READ_ONLY"; LOW_RISK="LOW_RISK"; MEDIUM_RISK="MEDIUM_RISK"; HIGH_RISK="HIGH_RISK"; CRITICAL="CRITICAL"
class AutonomyLevel(str, Enum):
    L0="L0"; L1="L1"; L2="L2"; L3="L3"; L4="L4"; L5="L5"
class ExecutionStatus(str, Enum):
    PLANNED="PLANNED"; AUTHORIZED="AUTHORIZED"; PREPARING="PREPARING"; RUNNING="RUNNING"; VERIFYING="VERIFYING"; COMPLETED="COMPLETED"; FAILED="FAILED"; PAUSED="PAUSED"; ESCALATED="ESCALATED"; ROLLED_BACK="ROLLED_BACK"; CANCELLED="CANCELLED"
class VerificationStatus(str, Enum): SUCCESS="SUCCESS"; PARTIAL_SUCCESS="PARTIAL_SUCCESS"; FAILED="FAILED"; UNKNOWN="UNKNOWN"

@dataclass(frozen=True)
class Authorization:
    permission: str; policy: str; autonomy: AutonomyLevel; approved: bool=False; human_required: bool=False

@dataclass(frozen=True)
class ActionRequest:
    action_id: str; action_type: str; target: str; parameters: dict[str, Any]; requested_by: str
    risk_level: RiskLevel; authorization: Authorization; allowed_targets: tuple[str,...]=(); allowed_actions: tuple[str,...]=(); allowed_channels: tuple[str,...]=(); idempotency_key: str=""
    cost: float=0.0; timeout_seconds: int=60; max_retries: int=0; data_classification: str="internal"

@dataclass(frozen=True)
class PlanTask:
    task_id: str; dependencies: tuple[str,...]; actions: tuple[ActionRequest,...]; verification: tuple[str,...]=(); rollback: tuple[str,...]=()

@dataclass(frozen=True)
class ExecutionPlan:
    plan_id: str; goal: str; tasks: tuple[PlanTask,...]; max_parallel_tasks: int=1; max_duration_seconds: int=300; max_total_cost: float=0.0; delegation_depth: int=0; max_delegation_depth: int=0

@dataclass
class ExecutionResult:
    execution_id: str; status: ExecutionStatus; verification: VerificationStatus=VerificationStatus.UNKNOWN; result: Any=None; error: Optional[str]=None; retries: int=0; rollback: Optional[dict[str,Any]]=None; incident_reference: Optional[str]=None
