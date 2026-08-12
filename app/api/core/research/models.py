from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class ResearchQuestion:
    research_question_id: str
    question: str
    objective: str
    scope: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    priority: str = "MEDIUM"
    risk: str = "LOW"
    status: str = "OPEN"
    owner: Optional[str] = None
    created_at: Optional[str] = None
    question_type: str = "UNKNOWN"
    sub_questions: List[str] = field(default_factory=list)
    evidence_requirements: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ResearchProject:
    project_id: str
    name: str
    objective: str
    question_ids: List[str] = field(default_factory=list)
    budget: Optional[float] = None
    resource: Dict[str, Any] = field(default_factory=dict)
    expected_value: Optional[float] = None
    status: str = "OPEN"

@dataclass(frozen=True)
class Source:
    source_id: str
    source_type: str
    title: str
    publisher: Optional[str] = None
    author_if_known: Optional[str] = None
    publication_date_if_known: Optional[str] = None
    retrieved_at: Optional[str] = None
    language: Optional[str] = None
    url_reference_if_available: Optional[str] = None
    trust_status: str = "UNKNOWN"
    verification_status: str = "UNVERIFIED"
    authority: Optional[float] = None
    relevance: Optional[float] = None
    recency: Optional[float] = None
    methodology: Optional[float] = None
    transparency: Optional[float] = None
    independence: Optional[float] = None

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    claim: str
    source_id: str
    support_type: str
    strength: str
    context: str
    location_if_available: Optional[str] = None
    confidence: Optional[float] = None

@dataclass(frozen=True)
class Claim:
    claim_id: str
    claim: str
    claim_type: str
    evidence_ids: List[str] = field(default_factory=list)
    confidence: Optional[float] = None
    status: str = "UNVERIFIED"

@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    statement: str
    rationale: str
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    testable_prediction: Optional[str] = None
    confidence: Optional[float] = None
    status: str = "PROPOSED"

@dataclass(frozen=True)
class Experiment:
    experiment_id: str
    objective: str
    hypothesis: str
    variables: Dict[str, Any] = field(default_factory=dict)
    method: str = ""
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None
    limitations: List[str] = field(default_factory=list)
    status: str = "DRAFT"
    authorization: Optional[str] = None

@dataclass(frozen=True)
class ResearchFinding:
    finding_id: str
    title: str
    known: List[str] = field(default_factory=list)
    likely: List[str] = field(default_factory=list)
    uncertain: List[str] = field(default_factory=list)
    unknown: List[str] = field(default_factory=list)
    claim_ids: List[str] = field(default_factory=list)
    status: str = "UNVERIFIED"
    expiration: Optional[str] = None
    review_date: Optional[str] = None

@dataclass(frozen=True)
class ResearchReview:
    review_id: str
    subject_id: str
    reviewer: str
    review_type: str
    accuracy: str
    evidence: str
    logic: str
    source_quality: str
    missing_context: str
    contradictions: str
    uncertainty: str
    citation: str
    decision: str = "INCONCLUSIVE"

@dataclass(frozen=True)
class KnowledgeGap:
    gap_id: str
    question: str
    importance: str
    risk: str
    frequency: Optional[float] = None
    business_impact: Optional[str] = None
    customer_impact: Optional[str] = None
    uncertainty: Optional[str] = None
    known_information: List[str] = field(default_factory=list)
    unknown_information: List[str] = field(default_factory=list)
    next_research_action: Optional[str] = None
