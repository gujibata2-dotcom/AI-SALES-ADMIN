def validate_knowledge_update(finding_status: str, review_decision: str, approval: str | None) -> dict:
    allowed = finding_status == "VALIDATED" and review_decision == "APPROVE" and bool(approval)
    return {"publish_allowed": allowed, "reason": "APPROVAL_REQUIRED" if not allowed else "VALIDATED_AND_APPROVED"}
