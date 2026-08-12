def validate(evidence: bool, prototype: bool, testing: bool, metrics: bool, risk_review: bool) -> str:
    return "VALIDATED" if all((evidence, prototype, testing, metrics, risk_review)) else "UNVERIFIED"
