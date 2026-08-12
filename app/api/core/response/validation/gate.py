from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    failures: tuple[str, ...]


def validate(*, factual: bool, grounded: bool, language: bool, tone: bool, ethics: bool, safety: bool, privacy: bool, sales_pressure: bool, claims_supported: bool) -> ValidationResult:
    checks = {"FACTUALITY": factual, "GROUNDING": grounded, "LANGUAGE": language, "TONE": tone, "ETHICS": ethics, "SAFETY": safety, "PRIVACY": privacy, "SALES_PRESSURE": sales_pressure, "CLAIMS": claims_supported}
    failures = tuple(name for name, passed in checks.items() if not passed)
    return ValidationResult(not failures, failures)
