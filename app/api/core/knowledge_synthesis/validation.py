"""Deterministic validation rules for Phase 39.
These checks are intentionally conservative: uncertainty is preserved instead of filled.
"""
from .contracts import KnowledgeRecord, KnowledgeStatus

def validate_for_verified(record: KnowledgeRecord, evidence_quality: float) -> tuple[bool, list[str]]:
    errors=[]
    if not record.provenance: errors.append('missing provenance')
    if not record.evidence: errors.append('missing evidence')
    if not record.statement.strip(): errors.append('missing statement')
    if not 0 <= record.confidence <= 1: errors.append('invalid confidence')
    if evidence_quality < 0.7: errors.append('evidence quality below verification threshold')
    if errors: return False, errors
    return True, []

def contradiction_classification(*, same_scope: bool, same_definition: bool, same_period: bool, same_measurement: bool, unresolved: bool=False) -> str:
    if unresolved: return 'unresolved'
    if not same_scope: return 'context_difference'
    if not same_definition: return 'definition_difference'
    if not same_period: return 'time_difference'
    if not same_measurement: return 'measurement_difference'
    return 'true_contradiction'

def confidence_label(confidence: float) -> str:
    if confidence >= .8: return 'HIGH'
    if confidence >= .5: return 'MEDIUM'
    return 'LOW'

def verification_status(record: KnowledgeRecord, quality: float) -> KnowledgeStatus:
    ok, _ = validate_for_verified(record, quality)
    return KnowledgeStatus.VERIFIED if ok else KnowledgeStatus.PARTIALLY_VERIFIED
