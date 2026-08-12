from app.api.core.economy.engine import EconomyEngine
from app.api.core.economy.budget import classify_budget
from app.api.core.economy.capacity import utilization


def test_unknown_cost():
    assert EconomyEngine().cost_status(None, False) == "COST_UNKNOWN"

def test_roi_requires_evidence():
    assert EconomyEngine().roi(None, 10)["status"] == "ROI_UNDETERMINED"

def test_budget_warning():
    assert classify_budget({"limit": 100, "spent": 90}) == "BUDGET_WARNING"

def test_capacity_gap():
    assert EconomyEngine().capacity_gap(120, 100)["status"] == "CAPACITY_GAP"

def test_utilization_unknown():
    assert utilization(None, 100)["status"] == "NOT_PROVIDED"

def test_financial_action_requires_approval():
    assert not EconomyEngine().authorize_financial_action(None, "PURCHASE")["allowed"]
