from app.api.core.response.decision.model import DecisionInput, DecisionType, decide


def test_human_request_escalates():
    result = decide(DecisionInput("product", "neutral", .9, True, "grounded", asks_for_human=True))
    assert result.type == DecisionType.ESCALATE


def test_no_knowledge_does_not_fabricate():
    result = decide(DecisionInput("price", "neutral", .9, False, "insufficient_evidence"))
    assert result.type == DecisionType.SAFE_UNKNOWN


def test_recommendation_without_knowledge_clarifies():
    result = decide(DecisionInput("recommendation", "neutral", .9, False, "insufficient_evidence"))
    assert result.type == DecisionType.CLARIFY


def test_sales_intent_alone_does_not_force_recommendation():
    result = decide(DecisionInput("purchase", "neutral", .9, False, "insufficient_evidence"))
    assert result.type != DecisionType.RECOMMEND
