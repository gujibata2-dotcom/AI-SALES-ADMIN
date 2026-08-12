from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class Problem:
    problem_id: str
    description: str
    context: str = ""
    affected_area: str = ""
    evidence: List[str] = field(default_factory=list)
    severity: Optional[float] = None
    frequency: Optional[float] = None
    constraints: List[str] = field(default_factory=list)
    status: str = "DISCOVERED"

@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    problem_id: str
    description: str
    potential_value: Optional[float] = None
    evidence: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    priority: str = "MEDIUM"
    confidence: Optional[float] = None
    status: str = "DISCOVERED"
    dimensions: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Idea:
    idea_id: str
    problem: str
    solution: str
    rationale: str
    evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    expected_benefit: str = ""
    risks: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    generation_method: str = "RECOMBINATION"
    novelty_status: str = "UNKNOWN"

@dataclass(frozen=True)
class Design:
    design_id: str
    idea_id: str
    requirements: Dict[str, List[str]] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    architecture: Dict[str, Any] = field(default_factory=dict)
    components: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    test_plan: List[str] = field(default_factory=list)
    version: str = "1.0"

@dataclass(frozen=True)
class Prototype:
    prototype_id: str
    version: str
    design_id: str
    components: List[str] = field(default_factory=list)
    objective: str = ""
    limitations: List[str] = field(default_factory=list)
    test_status: str = "NOT_TESTED"
    created_at: Optional[str] = None

@dataclass(frozen=True)
class InnovationExperiment:
    experiment_id: str
    prototype_id: str
    hypothesis: str
    variables: Dict[str, Any] = field(default_factory=dict)
    baseline: str = ""
    method: str = ""
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    limitations: List[str] = field(default_factory=list)
    conclusion: str = "UNKNOWN"
    status: str = "DRAFT"
    authorization: Optional[str] = None

@dataclass(frozen=True)
class Invention:
    invention_id: str
    name: str
    problem: str
    principle: str
    design: str
    novelty_status: str = "UNKNOWN"
    supporting_evidence: List[str] = field(default_factory=list)
    prototype: Optional[str] = None
    validation: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    status: str = "CONCEPT"

@dataclass(frozen=True)
class InnovationReview:
    review_id: str
    subject_id: str
    reviewer: str
    review_type: str
    evidence: str = ""
    prototype: str = ""
    testing: str = ""
    metrics: str = ""
    risk: str = ""
    decision: str = "INCONCLUSIVE"

@dataclass(frozen=True)
class InnovationRisk:
    risk_id: str
    subject_id: str
    technical_risk: str = "UNKNOWN"
    security_risk: str = "UNKNOWN"
    privacy_risk: str = "UNKNOWN"
    operational_risk: str = "UNKNOWN"
    financial_risk: str = "UNKNOWN"
    safety_risk: str = "UNKNOWN"
    reputational_risk: str = "UNKNOWN"
    mitigations: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class InnovationMetric:
    metric_id: str
    name: str
    baseline: Optional[float] = None
    candidate: Optional[float] = None
    unit: str = ""
    direction: str = "HIGHER_IS_BETTER"
    context: str = ""
