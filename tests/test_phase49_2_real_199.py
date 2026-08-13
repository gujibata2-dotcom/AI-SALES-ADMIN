import json
import os

import pytest

from app.api.customer_runtime.runtime import CustomerRuntime, PaymentVerificationError, Store


def session(tenant, price="price_199", amount=19900, currency="thb", payment_status="paid"):
    return {
        "id": "cs_test_real_199",
        "client_reference_id": tenant,
        "metadata": {"tenant_id": tenant, "plan_id": "199"},
        "payment_status": payment_status,
        "amount_total": amount,
        "currency": currency,
        "subscription": "sub_test_199",
        "line_items": {"data": [{"price": {"id": price}}]},
    }


def build(tmp_path, monkeypatch):
    monkeypatch.setenv("AI_DB_PATH", str(tmp_path / "test.sqlite3"))
    monkeypatch.setenv("STRIPE_PRICE_199_ID", "price_199")
    return CustomerRuntime(Store())


def test_verified_payment_activates_once(tmp_path, monkeypatch):
    runtime = build(tmp_path, monkeypatch)
    runtime.activate_199("tenant-a", "cs_test_real_199", "evt_1", session("tenant-a"))
    runtime.activate_199("tenant-a", "cs_test_real_199", "evt_1", session("tenant-a"))
    rows = runtime.store.db.execute("SELECT * FROM subscriptions WHERE tenant_id='tenant-a'").fetchall()
    tx = runtime.store.db.execute("SELECT * FROM billing_transactions WHERE payment_reference='cs_test_real_199'").fetchone()
    assert len(rows) == 1
    assert tx["status"] == "PAYMENT_SUCCEEDED"


@pytest.mark.parametrize("field, value, error", [
    ("amount_total", 10000, "PAYMENT_AMOUNT_MISMATCH"),
    ("currency", "usd", "PAYMENT_CURRENCY_MISMATCH"),
    ("payment_status", "unpaid", "PAYMENT_NOT_SETTLED"),
    ("client_reference_id", "tenant-b", "PAYMENT_CUSTOMER_MISMATCH"),
])
def test_payment_verification_rejects_tampering(tmp_path, monkeypatch, field, value, error):
    runtime = build(tmp_path, monkeypatch)
    payload = session("tenant-a")
    payload[field] = value
    with pytest.raises(PaymentVerificationError, match=error):
        runtime.activate_199("tenant-a", "cs_tampered", "evt_tampered", payload)


def test_payment_plan_mismatch_rejected(tmp_path, monkeypatch):
    runtime = build(tmp_path, monkeypatch)
    with pytest.raises(PaymentVerificationError, match="PAYMENT_PLAN_MISMATCH"):
        runtime.activate_199("tenant-a", "cs_wrong_plan", "evt_wrong_plan", session("tenant-a", price="price_other"))


def test_live_199_e2e_requires_explicit_production_credentials():
    required = [
        "STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET",
        "STRIPE_PRICE_199_ID",
        "MODEL_API_KEY",
        "MODEL_BASE_URL",
    ]
    if not all(os.getenv(k) for k in required):
        pytest.skip("LIVE_199_CREDENTIALS_NOT_CONFIGURED")
    pytest.fail("Live E2E must be executed against the deployed production/staging endpoint, not inside a unit test process")
