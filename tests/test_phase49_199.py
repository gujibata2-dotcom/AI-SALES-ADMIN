import json

import pytest

from app.api.core.production.runtime import TenantStore
from app.api.core.service.service import ServiceEngine
from app.api.core.phase49.gateway import Customer199Gateway, ProductReadiness
from app.api.core.phase49.payments import PaymentAdapter, PaymentEvent
from app.api.core.phase49.providers import MockModelProvider


class FakePayment(PaymentAdapter):
    configured = True
    live = False

    def checkout_url(self, tenant_id, package_id, success_url, cancel_url):
        return f"MOCKED://checkout/{tenant_id}/{package_id}"

    def verify_event(self, payload, signature):
        data = json.loads(payload)
        return PaymentEvent(data["id"], "checkout.session.completed", data["tenant_id"], "STARTER_199", True, 199, "pay_mock", data)


def build():
    service = ServiceEngine(store=TenantStore())
    return service, Customer199Gateway(service, FakePayment(), MockModelProvider("verified response"))


def test_199_requires_verified_payment_before_employee_work():
    service, gateway = build()
    gateway.begin_199_checkout("tenant-a", "https://ok", "https://cancel")
    with pytest.raises(PermissionError, match="STARTER_199_ENTITLEMENT_REQUIRED"):
        gateway.create_employee("tenant-a")
    gateway.apply_payment_event(b'{"id":"evt_1","tenant_id":"tenant-a"}', "mock")
    employee = gateway.create_employee("tenant-a")
    assert employee.startswith("tenant-a:sales")


def test_199_e2e_knowledge_task_result_and_idempotency():
    service, gateway = build()
    gateway.begin_199_checkout("tenant-a", "https://ok", "https://cancel")
    gateway.apply_payment_event(b'{"id":"evt_1","tenant_id":"tenant-a"}', "mock")
    employee = gateway.create_employee("tenant-a")
    gateway.add_knowledge("tenant-a", "Product", "Price is 199 THB.", "customer://product")
    first = gateway.execute_task("tenant-a", employee, "Answer with the verified price.", idempotency_key="k1")
    second = gateway.execute_task("tenant-a", employee, "Answer with the verified price.", idempotency_key="k1")
    assert first["status"] == "COMPLETED"
    assert first == second
    assert gateway.get_result("tenant-a", first["task_id"])["verified"] is True
    assert service.usage.total("tenant-a", "tasks") == 1


def test_cross_tenant_result_access_is_denied():
    service, gateway = build()
    gateway.begin_199_checkout("tenant-a", "https://ok", "https://cancel")
    gateway.apply_payment_event(b'{"id":"evt_1","tenant_id":"tenant-a"}', "mock")
    employee = gateway.create_employee("tenant-a")
    result = gateway.execute_task("tenant-a", employee, "hello", idempotency_key="k1")
    with pytest.raises(PermissionError, match="CROSS_TENANT_ACCESS_DENIED"):
        gateway.get_result("tenant-b", result["task_id"])


def test_real_readiness_requires_live_payment_and_model():
    service, gateway = build()
    assert gateway.readiness().evaluate() == ProductReadiness.TESTABLE
