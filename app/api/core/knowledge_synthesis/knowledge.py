"""Phase 39 contracts and guardrails.

The package is intentionally dependency-light. It provides deterministic validation helpers
for knowledge objects and classification primitives without requiring network packages.
"""
from __future__ import annotations

from typing import Any

KNOWLEDGE_STATUSES = {"RAW","UNVERIFIED","PARTIALLY_VERIFIED","VERIFIED","CONTESTED","OUTDATED","SUPERSEDED","REJECTED","UNKNOWN"}
CLAIM_TYPES = {"FACT","OBSERVATION","INFERENCE","HYPOTHESIS","OPINION","PREDICTION","UNKNOWN"}
ACCESS_LEVELS = {"PUBLIC","INTERNAL","RESTRICTED","CONFIDENTIAL"}


def validate_knowledge(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("knowledge_id","title","statement","domain","evidence","confidence","scope","limitations","version","status")
    errors.extend(f"missing:{k}" for k in required if k not in record)
    if "status" in record and record["status"] not in KNOWLEDGE_STATUSES: errors.append("invalid:status")
    if "confidence" in record and not isinstance(record["confidence"], (int,float)): errors.append("invalid:confidence")
    if isinstance(record.get("confidence"), (int,float)) and not 0 <= record["confidence"] <= 1: errors.append("range:confidence")
    if not record.get("evidence") and record.get("status") == "VERIFIED": errors.append("verified_without_evidence")
    return errors


def classify_claim(has_direct_evidence: bool, is_observed: bool = False, is_explicitly_uncertain: bool = False) -> str:
    if is_explicitly_uncertain and not has_direct_evidence: return "UNKNOWN"
    if has_direct_evidence: return "FACT"
    if is_observed: return "OBSERVATION"
    return "INFERENCE"


def should_require_human_review(*, impact: float, risk: float, critical: bool = False, sensitive: bool = False, uncertain: bool = False) -> bool:
    return critical or sensitive or uncertain or impact >= 0.8 or risk >= 0.8
