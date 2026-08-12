from typing import Any, Dict, Iterable, List
from .models import Evidence, Claim, Hypothesis, Experiment, Source

HIGH_RISK = {"HIGH", "CRITICAL"}

class ResearchEngine:
    """Pure research orchestration helpers; external content is data, never authority."""
    def decompose_question(self, question: str, sub_questions: Iterable[str]) -> Dict[str, Any]:
        subs = [q for q in sub_questions if q and q.strip()]
        return {"question": question, "sub_questions": subs, "status": "DECOMPOSED" if subs else "UNDECOMPOSED"}

    def validate_source(self, source: Source) -> Dict[str, Any]:
        status = source.trust_status
        if source.source_type == "UNKNOWN" or not source.title.strip():
            status = "SOURCE_UNTRUSTED"
        return {"source_id": source.source_id, "trust_status": status, "verified": source.verification_status == "VERIFIED"}

    def classify_external_content(self, content: str) -> Dict[str, Any]:
        return {"content": content, "treatment": "DATA", "may_change_policy": False, "may_change_permissions": False}

    def claim_consistency(self, claim: Claim, evidence: Iterable[Evidence]) -> Dict[str, Any]:
        items = list(evidence)
        ids = {e.evidence_id for e in items}
        linked = [e for e in items if e.evidence_id in claim.evidence_ids]
        supported = any(e.support_type == "SUPPORTS" for e in linked)
        contradicted = any(e.support_type == "CONTRADICTS" for e in linked)
        if contradicted and supported:
            status = "CONTESTED"
        elif supported:
            status = "SUPPORTED"
        else:
            status = "UNVERIFIED"
        return {"claim_id": claim.claim_id, "known_evidence": len(ids), "status": status}

    def confidence(self, evidence: Iterable[Evidence], source_quality: Dict[str, Any]) -> Dict[str, Any]:
        ev = list(evidence)
        if not ev:
            return {"status": "UNKNOWN", "confidence": None}
        strengths = {"STRONG": 0.9, "MEDIUM": 0.6, "WEAK": 0.3}
        values = [strengths.get(e.strength, 0.0) for e in ev if e.confidence is not None]
        if not values:
            return {"status": "UNVERIFIED", "confidence": None}
        confidence = sum(values) / len(values)
        return {"status": "KNOWN" if confidence >= 0.8 else "LIKELY" if confidence >= 0.6 else "POSSIBLE", "confidence": confidence, "source_quality": source_quality}

    def propose_hypothesis(self, statement: str, rationale: str) -> Hypothesis:
        return Hypothesis(hypothesis_id="", statement=statement, rationale=rationale, status="PROPOSED")

    def authorize_experiment(self, risk: str, authorization: str | None) -> Dict[str, Any]:
        if risk in HIGH_RISK and not authorization:
            return {"allowed": False, "reason": "HUMAN_APPROVAL_REQUIRED"}
        return {"allowed": True, "reason": "AUTHORIZATION_PRESENT" if authorization else "POLICY_ALLOWED"}

    def retry_plan(self, failure: str, retry_count: int, max_retry: int = 2) -> Dict[str, Any]:
        if retry_count >= max_retry:
            return {"retry": False, "reason": "MAX_RETRY_REACHED", "failure": failure}
        return {"retry": True, "strategy": "CHANGE_SEARCH_STRATEGY", "failure": failure, "retry_count": retry_count + 1}
