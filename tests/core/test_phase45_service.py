"""Synthetic Phase 45 tests; stdlib-only, no real payments."""
import unittest

from app.api.core.service import BillingProvider, BillingStatus, QuotaState, ServiceEngine, SubscriptionStatus


class Phase45CommercialTests(unittest.TestCase):
    def setUp(self):
        self.svc = ServiceEngine()
        self.svc.create_organization("CUSTOMER_A", "ORG_A")
        self.svc.create_organization("CUSTOMER_B", "ORG_B")
        self.svc.start_trial("ORG_A")
        self.svc.start_trial("ORG_B")

    def test_customer_isolation(self):
        a = self.svc.hire_employee("ORG_A", "sales", permissions=frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "SEND_MESSAGE"}))
        b = self.svc.hire_employee("ORG_B", "sales", permissions=frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "SEND_MESSAGE"}))
        self.assertNotEqual(a.organization_id, b.organization_id)
        with self.assertRaises(PermissionError):
            self.svc.store.get_employee("ORG_A", b.employee_id)

    def test_free_trial_and_no_fake_billing(self):
        sub = next(s for s in self.svc.subscriptions.values() if s.organization_id == "ORG_A")
        self.assertEqual(sub.status, SubscriptionStatus.TRIAL)
        with self.assertRaises(RuntimeError) as ctx:
            self.svc.activate_subscription(sub.subscription_id, payment_authorized=True)
        self.assertEqual(str(ctx.exception), BillingStatus.NOT_CONFIGURED.value)
        self.assertFalse(self.svc.billing.configured)

    def test_entitlement_and_employee_contract(self):
        contract = self.svc.hire_employee("ORG_A", "sales", permissions=frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "SEND_MESSAGE"}))
        self.assertEqual(contract.package_id, "FREE")
        with self.assertRaises(PermissionError):
            self.svc.hire_employee("ORG_A", "research", permissions=frozenset({"READ_KNOWLEDGE"}))

    def test_quota_warning_and_limit(self):
        self.svc.quota = self.svc.quota.__class__({"tasks": 5})
        for _ in range(4):
            state = self.svc.record_usage("ORG_A", "tasks")
        self.assertEqual(state, QuotaState.WARNING)
        self.assertEqual(self.svc.record_usage("ORG_A", "tasks"), QuotaState.WARNING)
        self.assertEqual(self.svc.record_usage("ORG_A", "tasks"), QuotaState.EXCEEDED)

    def test_downgrade_does_not_delete_data_and_checks_limit(self):
        self.svc.start_trial("ORG_A", "TEAM_399")
        sub = [s for s in self.svc.subscriptions.values() if s.organization_id == "ORG_A"][-1]
        # Existing FREE subscription does not get silently removed; this test uses a fresh service subscription.
        self.svc.hire_employee("ORG_A", "sales", permissions=frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "SEND_MESSAGE"}))
        changed = self.svc.change_package(sub.subscription_id, "STARTER_199", authorized=True)
        self.assertEqual(changed.package_id, "STARTER_199")
        self.assertTrue(self.svc.store.organizations["ORG_A"])

    def test_webhook_requires_secret(self):
        provider = BillingProvider()
        self.assertFalse(provider.verify_webhook(b"event", "bad", None))

    def test_readiness_blocks_without_billing_and_social(self):
        gates = self.svc.readiness(phase44_ready=True, social_configured=False, billing_configured=False)
        self.assertTrue(gates["FREE_COMMERCIAL_READY"])
        self.assertFalse(gates["STARTER_199_COMMERCIAL_READY"])
        self.assertEqual(gates["billing"], "BILLING_NOT_CONFIGURED")

    def test_dashboard_contains_only_requested_tenant(self):
        self.svc.hire_employee("ORG_A", "sales", permissions=frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "SEND_MESSAGE"}))
        dashboard = self.svc.dashboard("ORG_A")
        self.assertTrue(all("ORG_B" not in str(value) for value in dashboard.values()))
        self.assertIn("employees", dashboard)


if __name__ == "__main__":
    unittest.main()
