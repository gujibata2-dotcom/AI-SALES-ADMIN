"""Non-bypassable policy boundaries for the Phase 12 learning layer.

This module is intentionally small and dependency-free. It defines what learning
may propose and what it can never authorize. It does not publish or deploy.
"""

from dataclasses import dataclass

FORBIDDEN_IMPROVEMENT_SIGNALS = frozenset({
    "deception",
    "fake urgency",
    "fake scarcity",
    "emotional manipulation",
    "hide uncertainty",
    "hide stock",
    "reduce safety",
    "disable ethics",
    "bypass human approval",
    "change source authority",
    "autonomous publishing",
    "autonomous deployment",
    "sensitive profiling",
})

APPROVAL_REQUIRED_TYPES = frozenset({
    "KNOWLEDGE_UPDATE",
    "FAQ_UPDATE",
    "RETRIEVAL_UPDATE",
    "PROMPT_UPDATE",
    "RESPONSE_POLICY_UPDATE",
    "WORKFLOW_UPDATE",
    "SALES_POLICY_UPDATE",
    "CLARIFICATION_UPDATE",
})


@dataclass(frozen=True)
class LearningProposal:
    recommendation_id: str
    recommendation_type: str
    proposed_change: str
    requires_human_approval: bool = True


def validate_proposal(proposal: LearningProposal) -> tuple[bool, str]:
    """Return whether a proposal is admissible for human review.

    Admissible means only that it can enter review; it is not approval and does
    not authorize publishing.
    """
    text = proposal.proposed_change.casefold()
    for signal in FORBIDDEN_IMPROVEMENT_SIGNALS:
        if signal in text:
            return False, f"blocked safety/ethics signal: {signal}"
    if proposal.recommendation_type in APPROVAL_REQUIRED_TYPES and not proposal.requires_human_approval:
        return False, "human approval is mandatory for material learning changes"
    return True, "eligible for human review only"
