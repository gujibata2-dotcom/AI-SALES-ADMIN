import json
from pathlib import Path
from app.api.core.innovation.engine import InnovationEngine
from app.api.core.innovation.knowledge_combination.engine import combine
from app.api.core.innovation.failure.engine import analyze_failure
from app.api.core.innovation.feasibility.engine import assess_feasibility
from app.api.core.innovation.ip_review.engine import review_ip
from app.api.core.innovation.security.guards import security_guard


def test_lifecycle_and_novelty():
    e = InnovationEngine()
    assert e.LIFECYCLE[0] == "RESEARCH"
    assert e.novelty(False, False) == "PRIOR_ART_UNKNOWN"
    assert e.novelty(False, True) == "POTENTIALLY_NEW"


def test_validation_requires_all_evidence_gates():
    e = InnovationEngine()
    assert e.validate(True, True, True, True, True) == "VALIDATED"
    assert e.validate(True, True, True, False, True) == "UNVERIFIED"


def test_high_risk_deployment_requires_human_approval():
    e = InnovationEngine()
    assert not e.authorize_deployment("HIGH", None)
    assert e.authorize_deployment("HIGH", "APPROVED")


def test_baseline_required_for_better_claim():
    e = InnovationEngine()
    assert e.baseline_claim("speed", None, 10)["status"] == "UNKNOWN"
    assert e.baseline_claim("speed", 10, 12)["delta"] == 2


def test_failure_does_not_claim_root_cause():
    assert analyze_failure(["timeout"], ["network", "model"])["root_cause"] == "UNKNOWN"


def test_feasibility_and_ip_boundary():
    assert assess_feasibility("FEASIBLE", "FEASIBLE", "FEASIBLE", "FEASIBLE")["result"] == "FEASIBLE"
    assert review_ip(False)["patentability"] == "UNKNOWN"


def test_security_guard_blocks_obvious_unsafe_execution():
    assert security_guard("eval(payload)")["allowed"] is False
    assert security_guard("safe declarative prototype")["allowed"] is True


def test_schema_json_valid():
    root = Path(__file__).parents[1] / "schemas"
    for p in root.glob("*.schema.json"):
        obj = json.loads(p.read_text(encoding="utf-8"))
        assert obj["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_knowledge_combination_is_not_declared_new():
    result = combine(["knowledge-a", "knowledge-b"], "shared constraint", ["assumption"])
    assert result["novelty_status"] == "UNKNOWN"
