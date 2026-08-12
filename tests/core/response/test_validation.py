from app.api.core.response.validation.gate import validate


def test_validation_blocks_unsupported_claims():
    result = validate(factual=True, grounded=True, language=True, tone=True, ethics=True, safety=True, privacy=True, sales_pressure=True, claims_supported=False)
    assert not result.passed
    assert "CLAIMS" in result.failures
