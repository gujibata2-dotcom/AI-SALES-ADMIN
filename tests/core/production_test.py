import unittest

from app.api.core.production.runtime import (
    AuditLog, Authorization, Employee, EmployeeRuntime, EmployeeStatus,
    KillSwitch, ModelRouter, Quota, Task, TaskStatus, TenantStore,
)


class ProductionRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.store = TenantStore()
        self.store.add_employee(Employee(
            employee_id="emp-a", organization_id="org-a", role="Sales",
            permissions=frozenset({"SEND_MESSAGE"}),
        ))
        self.store.add_employee(Employee(
            employee_id="emp-b", organization_id="org-b", role="Sales",
            permissions=frozenset({"SEND_MESSAGE"}),
        ))
        self.runtime = EmployeeRuntime(
            self.store,
            Authorization({"SEND_MESSAGE": {"SEND_MESSAGE"}}),
            Quota({"tasks": 2}),
            ModelRouter({"answer": "configured-test-model"}),
            KillSwitch(),
            AuditLog(),
        )
        self.runtime.activate("org-a", "emp-a")

    def test_employee_activation_requires_permission(self):
        self.store.add_employee(Employee("emp-no", "org-a", "Support"))
        with self.assertRaises(PermissionError):
            self.runtime.activate("org-a", "emp-no")

    def test_task_requires_authorization(self):
        task = Task("t1", "org-a", "emp-a", "answer", "DELETE_DATABASE", idempotency_key="t1")
        result = self.runtime.execute(task, lambda _: "bad", verify=lambda _: True)
        self.assertEqual(result.status, TaskStatus.REQUIRES_HUMAN)

    def test_completion_requires_verification(self):
        task = Task("t2", "org-a", "emp-a", "answer", "SEND_MESSAGE", idempotency_key="t2")
        result = self.runtime.execute(task, lambda _: "ok", verify=lambda _: False)
        self.assertEqual(result.status, TaskStatus.UNKNOWN)
        self.assertFalse(result.verified)

    def test_verified_completion(self):
        task = Task("t3", "org-a", "emp-a", "answer", "SEND_MESSAGE", idempotency_key="t3")
        result = self.runtime.execute(task, lambda _: "ok", verify=lambda value: value == "ok")
        self.assertEqual(result.status, TaskStatus.COMPLETED)
        self.assertTrue(result.verified)

    def test_idempotency_prevents_duplicate_execution(self):
        calls = []
        task = Task("t4", "org-a", "emp-a", "answer", "SEND_MESSAGE", idempotency_key="same")
        self.runtime.execute(task, lambda _: calls.append(1) or "ok", verify=lambda _: True)
        self.runtime.execute(task, lambda _: calls.append(1) or "ok", verify=lambda _: True)
        self.assertEqual(calls, [1])

    def test_quota_blocks_excess_tasks(self):
        for i in range(2):
            task = Task(f"qt{i}", "org-a", "emp-a", "answer", "SEND_MESSAGE", idempotency_key=f"qt{i}")
            self.runtime.execute(task, lambda _: "ok", verify=lambda _: True)
        task = Task("qt2", "org-a", "emp-a", "answer", "SEND_MESSAGE", idempotency_key="qt2")
        result = self.runtime.execute(task, lambda _: "ok", verify=lambda _: True)
        self.assertEqual(result.status, TaskStatus.BLOCKED)
        self.assertEqual(result.reason, "QUOTA_LIMIT")

    def test_kill_switch_stops_employee(self):
        self.runtime.kill_switch.stop("employee", "emp-a")
        task = Task("kill", "org-a", "emp-a", "answer", "SEND_MESSAGE", idempotency_key="kill")
        result = self.runtime.execute(task, lambda _: "ok", verify=lambda _: True)
        self.assertEqual(result.reason, "KILL_SWITCH")

    def test_cross_tenant_access_denied(self):
        with self.assertRaises(PermissionError):
            self.store.get_employee("org-b", "emp-a")

    def test_model_not_configured_is_not_success(self):
        task = Task("m1", "org-a", "emp-a", "research", "SEND_MESSAGE", idempotency_key="m1")
        result = self.runtime.execute(task, lambda _: "ok", verify=lambda _: True)
        self.assertEqual(result.status, TaskStatus.UNKNOWN)
        self.assertEqual(result.reason, "MODEL_NOT_CONFIGURED")

    def test_audit_created_for_actions(self):
        task = Task("audit", "org-a", "emp-a", "answer", "SEND_MESSAGE", idempotency_key="audit")
        self.runtime.execute(task, lambda _: "ok", verify=lambda _: True)
        self.assertGreaterEqual(len(self.runtime.audit.events), 2)
        self.assertTrue(all(event.organization_id == "org-a" for event in self.runtime.audit.events))


if __name__ == "__main__":
    unittest.main()
