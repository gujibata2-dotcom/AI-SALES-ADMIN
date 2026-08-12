"""Explicit integration contracts for prior phases; adapters are side-effect free."""
from typing import Any, Dict

def knowledge_update_proposal(finding_id: str, previous_version: str | None, evidence_ids: list[str], reason: str) -> Dict[str, Any]:
    return {"target": "PHASE_3_KNOWLEDGE", "finding_id": finding_id, "previous_version": previous_version, "new_evidence": evidence_ids, "reason": reason, "approval_required": True}

def learning_outcome(method: str, outcome: str, dimensions: Dict[str, Any]) -> Dict[str, Any]:
    return {"target": "PHASE_12_LEARNING", "method": method, "outcome": outcome, "dimensions": dimensions}

def workforce_assignment(role: str, capability: str, risk: str) -> Dict[str, Any]:
    return {"target": "PHASE_33_WORKFORCE", "role": role, "capability": capability, "risk": risk, "requires_governance": risk in {"HIGH", "CRITICAL"}}

def organization_decision(insight: str, evidence_ids: list[str]) -> Dict[str, Any]:
    return {"target": "PHASE_34_ORGANIZATION", "insight": insight, "evidence_ids": evidence_ids, "decision": "RECOMMENDATION_ONLY"}

def capability_investment(gap: str, cost: Any, value: Any) -> Dict[str, Any]:
    return {"target": "PHASE_35_ECONOMY", "capability_gap": gap, "cost": cost, "value": value, "status": "ROI_UNDETERMINED" if cost is None or value is None else "READY_FOR_ANALYSIS"}
