from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class Resource:
    resource_id: str
    type: str
    provider: Optional[str] = None
    capacity: Optional[float] = None
    unit: Optional[str] = None
    cost_model: Dict[str, Any] = field(default_factory=dict)
    availability: Optional[float] = None
    limits: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    status: str = "UNKNOWN"

@dataclass
class Budget:
    budget_id: str
    owner: str
    period: str
    limit: Optional[float] = None
    allocated: float = 0.0
    reserved: float = 0.0
    spent: float = 0.0
    status: str = "DRAFT"
    approval: Optional[str] = None

@dataclass(frozen=True)
class CostRecord:
    cost_id: str
    amount: Optional[float]
    currency: Optional[str] = None
    source: Optional[str] = None
    status: str = "NOT_PROVIDED"
    organization_id: Optional[str] = None
    project_id: Optional[str] = None
    team_id: Optional[str] = None
    employee_id: Optional[str] = None
    task_id: Optional[str] = None
    execution_id: Optional[str] = None

@dataclass(frozen=True)
class Allocation:
    allocation_id: str
    resource_id: str
    target_id: str
    requested: Optional[float]
    approved: Optional[float]
    authority: Optional[str]
    status: str = "RECOMMENDED"

@dataclass(frozen=True)
class CapacitySnapshot:
    resource_id: str
    current_capacity: Optional[float]
    required_capacity: Optional[float]
    future_capacity: Optional[float]
    reserved_capacity: Optional[float]
    unused_capacity: Optional[float]
    status: str = "UNKNOWN"

@dataclass(frozen=True)
class ValueRecord:
    value_id: str
    business_value: Optional[float] = None
    customer_value: Optional[float] = None
    time_saved: Optional[float] = None
    quality_gain: Optional[float] = None
    risk_reduction: Optional[float] = None
    verified_revenue_impact: Optional[float] = None
    cost_avoidance: Optional[float] = None
    status: str = "NOT_PROVIDED"

@dataclass(frozen=True)
class ROIRecord:
    roi_id: str
    investment_cost: Optional[float]
    verified_benefit: Optional[float]
    roi: Optional[float]
    status: str = "ROI_UNDETERMINED"
