from app.api.core.science.engine import ScienceEngine, Measurement, Hypothesis
from app.api.core.science.statistics.engine import descriptive
from app.api.core.science.causal.engine import avoid_causation_overclaim

def test_measurement_requires_source():
    try: Measurement("m","x",1,"u","method","").validate(); assert False
    except ValueError: assert True

def test_hypothesis_testability():
    assert Hypothesis("h","x","r",[],[]).testability()=="NOT_TESTABLE"

def test_no_fake_statistics():
    assert descriptive([])["status"]=="UNKNOWN"

def test_no_causation_overclaim():
    assert avoid_causation_overclaim(0.8,False)=="CORRELATION_ONLY"

def test_production_requires_approval():
    assert not ScienceEngine().authorize("PRODUCTION","LOW",None)
