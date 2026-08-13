"""Phase 41 integration facade.

This package extends app.api.core.decision rather than replacing it. Execution is
represented as a handoff contract to Phase 24; this module never performs tools,
financial actions, deployment, or external side effects.
"""
from .contracts import *
from .evaluation import *
from .strategy import *

PHASE_24_EXECUTION_BOUNDARY = "app.api.core.decision.execution"
PHASE_33_WORKFORCE_BOUNDARY = "app.api.core.organization"
PHASE_39_KNOWLEDGE_BOUNDARY = "app.api.core.knowledge_synthesis"


def execution_handoff(decision_id: str, action_reference: str, authorization_reference: str) -> dict[str, str]:
    if not authorization_reference:
        raise PermissionError("BLOCK: execution handoff requires authorization reference")
    return {"decision_id": decision_id, "action_reference": action_reference, "authorization_reference": authorization_reference, "target": PHASE_24_EXECUTION_BOUNDARY}


def decision_support(*, context: dict, evidence: list[EvidenceRef], objectives: list[str], constraints: list[Constraint], options: list[DecisionOption]) -> dict:
    if not evidence:
        uncertainty = Uncertainty.UNKNOWN
    elif any(not e.verified for e in evidence):
        uncertainty = Uncertainty.UNCERTAIN
    else:
        uncertainty = Uncertainty.KNOWN
    return {"type": "RECOMMENDATION", "context": context, "objectives": objectives, "constraints": constraints, "options": [o.option_id for o in options], "uncertainty": uncertainty.value, "authorized": False, "decision": None}
