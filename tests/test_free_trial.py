import unittest

from app.api.core.phase49.providers import MockModelProvider
from app.api.core.phase49.trial import FREE_TRIAL_DAYS, FreeTrialGateway
from app.api.core.service.service import ServiceEngine, SubscriptionStatus


class FreeTrialProductionValidationTests(unittest.TestCase):
    def setUp(self):
        self.service = ServiceEngine()
        self.model = MockModelProvider(response="ตอบจากข้อมูลธุรกิจของลูกค้า")
        self.gateway = FreeTrialGateway(self.service, self.model)

    def test_free_trial_is_30_days_and_unpaid(self):
        sub = self.gateway.start("tenant_a")
        self.assertEqual(sub.package_id, "FREE")
        self.assertEqual(sub.status, SubscriptionStatus.TRIAL)
        self.assertEqual(sub.trial_end_at - sub.start_at, FREE_TRIAL_DAYS * 86400)
        self.assertIsNone(sub.billing_reference)

    def test_real_trial_path_reaches_verified_result_with_mock_only(self):
        self.gateway.start("tenant_a")
        employee_id = self.gateway.create_employee("tenant_a", "sales")
        self.gateway.add_knowledge("tenant_a", "Product", "ราคา 199 บาท", "customer://product")
        result = self.gateway.execute_task("tenant_a", employee_id, "ตอบลูกค้าเรื่องราคา", idempotency_key="t1")
        self.assertEqual(result["status"], "COMPLETED")
        self.assertTrue(result["verified"])
        self.assertEqual(self.service.usage.total("tenant_a", "tasks"), 1)

    def test_idempotency_does_not_duplicate_execution(self):
        self.gateway.start("tenant_a")
        employee_id = self.gateway.create_employee("tenant_a")
        first = self.gateway.execute_task("tenant_a", employee_id, "งาน", idempotency_key="same")
        second = self.gateway.execute_task("tenant_a", employee_id, "งาน", idempotency_key="same")
        self.assertEqual(first, second)
        self.assertEqual(self.service.usage.total("tenant_a", "tasks"), 1)

    def test_cross_tenant_result_is_denied(self):
        self.gateway.start("tenant_a")
        employee_id = self.gateway.create_employee("tenant_a")
        result = self.gateway.execute_task("tenant_a", employee_id, "งาน", idempotency_key="t1")
        with self.assertRaises(PermissionError):
            self.gateway.get_result("tenant_b", result["task_id"])

    def test_mock_provider_cannot_claim_real_trial_readiness(self):
        self.gateway.start("tenant_a")
        self.gateway.create_employee("tenant_a")
        self.gateway.add_knowledge("tenant_a", "Product", "Known fact", "customer://product")
        readiness = self.gateway.readiness("tenant_a")
        self.assertFalse(readiness.ready_for_real_trial)
        self.assertFalse(readiness.model_connected)


if __name__ == "__main__":
    unittest.main()
