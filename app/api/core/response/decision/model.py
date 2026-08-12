from dataclasses import dataclass
from enum import Enum

class DecisionType(str, Enum):
    ANSWER="ANSWER"; CLARIFY="CLARIFY"; RECOMMEND="RECOMMEND"; COMPARE="COMPARE"
    SUPPORT="SUPPORT"; REFUSE="REFUSE"; ESCALATE="ESCALATE"; SAFE_UNKNOWN="SAFE_UNKNOWN"

@dataclass(frozen=True)
class DecisionInput:
    intent: str
    emotion: str
    confidence: float
    has_knowledge: bool
    knowledge_state: str
    asks_for_human: bool = False
    serious_complaint: bool = False
    legal_issue: bool = False
    payment_dispute: bool = False
    sensitive_situation: bool = False
    policy_violation: bool = False
    high_risk: bool = False

@dataclass(frozen=True)
class Decision:
    type: DecisionType
    reason: str
    requires_human_review: bool = False

def decide(value: DecisionInput) -> Decision:
    if value.asks_for_human or value.serious_complaint or value.legal_issue or value.payment_dispute or value.sensitive_situation or value.high_risk or value.policy_violation:
        return Decision(DecisionType.ESCALATE, "Human escalation rule matched.", True)
    if value.confidence < 0.5 or value.knowledge_state == "conflict":
        return Decision(DecisionType.CLARIFY, "Confidence or evidence is insufficient for a safe answer.")
    if value.intent in {"recommendation", "product_recommendation"} and not value.has_knowledge:
        return Decision(DecisionType.CLARIFY, "Recommendation requires verified product knowledge.")
    if value.intent == "comparison":
        return Decision(DecisionType.COMPARE, "Customer requested a comparison.")
    if value.intent in {"purchase", "ready_to_buy"} and value.has_knowledge:
        return Decision(DecisionType.RECOMMEND, "Purchase intent with grounded knowledge.")
    if not value.has_knowledge and value.intent in {"price", "product", "stock", "promotion"}:
        return Decision(DecisionType.SAFE_UNKNOWN, "No verified knowledge is available.")
    return Decision(DecisionType.ANSWER, "Answer using the grounded conversation context.")
