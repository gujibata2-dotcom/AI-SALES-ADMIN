"""Phase 45 customer-facing AI Employee service primitives.

Stdlib-only and provider-agnostic. Billing remains NOT_CONFIGURED until a
verified provider adapter is supplied. Reuses Phase 44 Employee/tenant
runtime concepts rather than creating a second execution engine.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from hmac import compare_digest
from time import time
from typing import Any, Mapping

from app.api.core.production.runtime import Employee, EmployeeStatus, TenantStore


class SubscriptionStatus(str, Enum):
    TRIAL = "TRIAL"; ACTIVE = "ACTIVE"; PAST_DUE = "PAST_DUE"; PAUSED = "PAUSED"; CANCELED = "CANCELED"; EXPIRED = "EXPIRED"; UNKNOWN = "UNKNOWN"
class EmployeeContractStatus(str, Enum):
    TRIAL = "TRIAL"; ACTIVE = "ACTIVE"; PAUSED = "PAUSED"; SUSPENDED = "SUSPENDED"; RETIRED = "RETIRED"
class QuotaState(str, Enum):
    AVAILABLE = "AVAILABLE"; WARNING = "WARNING"; LIMITED = "LIMITED"; EXCEEDED = "EXCEEDED"
class BillingStatus(str, Enum):
    NOT_CONFIGURED = "BILLING_NOT_CONFIGURED"; ACTIVE = "ACTIVE"; FAILED = "FAILED"; UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class Package:
    package_id: str; name: str; price_baht: int | None; billing_period: str; employee_limit: int | None; entitlements: Mapping[str, Any]

PACKAGES: dict[str, Package] = {
    "FREE": Package("FREE", "Free", 0, "trial", 1, {"employees": 1, "features": {"conversation", "product_knowledge", "basic_sales", "basic_content", "task_execution"}}),
    "STARTER_199": Package("STARTER_199", "Starter", 199, "monthly", 2, {"employees": 2, "features": {"sales", "support", "product_knowledge", "content", "automation", "memory", "learning", "social_commerce", "verification", "human_escalation"}}),
    "TEAM_399": Package("TEAM_399", "Team", 399, "monthly", 5, {"employees": 5, "features": {"sales", "support", "product_knowledge", "content", "automation", "memory", "learning", "social_commerce", "verification", "human_escalation", "team"}}),
    "DEPARTMENT_699": Package("DEPARTMENT_699", "AI Department", 699, "monthly", 10, {"employees": 10, "features": {"sales", "support", "content", "research", "operations", "automation", "learning", "social_commerce", "team", "analytics"}}),
    "ORGANIZATION_1499": Package("ORGANIZATION_1499", "AI Organization", 1499, "monthly", None, {"employees": "custom", "features": {"organization", "custom"}}),
}

@dataclass(frozen=True)
class EmployeeCatalogItem:
    employee_id: str; name: str; role: str; description: str; capabilities: frozenset[str]; limitations: frozenset[str]; required_permissions: frozenset[str]; available_packages: frozenset[str]; status: str = "AVAILABLE"; version: int = 1

CATALOG: dict[str, EmployeeCatalogItem] = {
    "sales": EmployeeCatalogItem("sales", "Sales Employee", "Sales", "Product-aware sales conversations and task execution.", frozenset({"sales", "product_knowledge"}), frozenset({"no_unverified_claims", "no_unauthorized_billing"}), frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "SEND_MESSAGE"}), frozenset(PACKAGES)),
    "support": EmployeeCatalogItem("support", "Support Employee", "Customer Support", "Customer support workflows with escalation.", frozenset({"support", "product_knowledge"}), frozenset({"no_irreversible_actions_without_approval"}), frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "SEND_MESSAGE"}), frozenset(PACKAGES)),
    "content": EmployeeCatalogItem("content", "Content Employee", "Content Creator", "Creates governed product content; publishing remains subject to configured adapters.", frozenset({"content", "product_knowledge"}), frozenset({"no_fake_claims", "no_unverified_publish"}), frozenset({"READ_PRODUCT", "READ_KNOWLEDGE", "CREATE_CONTENT"}), frozenset(PACKAGES)),
    "research": EmployeeCatalogItem("research", "Research Employee", "Researcher", "Research workflow bounded by available research capabilities.", frozenset({"research", "evidence"}), frozenset({"external_services_may_be_unconfigured"}), frozenset({"READ_KNOWLEDGE"}), frozenset({"DEPARTMENT_699", "ORGANIZATION_1499"})),
    "admin": EmployeeCatalogItem("admin", "Admin Employee", "Administrator", "Administrative task coordination under explicit permissions.", frozenset({"administration", "task_management"}), frozenset({"no_policy_change_by_default"}), frozenset({"READ_KNOWLEDGE"}), frozenset({"TEAM_399", "DEPARTMENT_699", "ORGANIZATION_1499"})),
}

@dataclass(frozen=True)
class Subscription:
    subscription_id: str; organization_id: str; package_id: str; status: SubscriptionStatus; start_at: float; renew_at: float | None = None; cancel_at: float | None = None; trial_end_at: float | None = None; billing_reference: str | None = None
@dataclass(frozen=True)
class EmployeeContract:
    contract_id: str; employee_id: str; organization_id: str; package_id: str; start_date: float; renewal_date: float | None; permissions: frozenset[str]; quota: Mapping[str, int]; status: EmployeeContractStatus; configuration: Mapping[str, Any]; version: int = 1
@dataclass(frozen=True)
class UsageEvent:
    usage_id: str; organization_id: str; employee_id: str | None; task_id: str | None; resource_type: str; quantity: int; timestamp: float
@dataclass(frozen=True)
class AuditEvent:
    event_id: str; organization_id: str; actor: str; action: str; result: str; timestamp: float; reference: str | None = None

class PackageEngine:
    def __init__(self, packages: Mapping[str, Package] | None = None): self.packages = dict(packages or PACKAGES)
    def get(self, package_id: str) -> Package: return self.packages[package_id]
    def can_hire(self, package_id: str, employee_kind: str, current_count: int) -> bool:
        package, item = self.get(package_id), CATALOG[employee_kind]
        return item.status == "AVAILABLE" and package_id in item.available_packages and (package.employee_limit is None or current_count < package.employee_limit)
    def has_feature(self, package_id: str, feature: str) -> bool: return feature in self.get(package_id).entitlements.get("features", set())

class QuotaEngine:
    def __init__(self, limits: Mapping[str, int]): self.limits = dict(limits); self.used: dict[tuple[str, str], int] = {}
    def state(self, organization_id: str, resource: str) -> QuotaState:
        limit, used = self.limits.get(resource), self.used.get((organization_id, resource), 0)
        if limit is None: return QuotaState.AVAILABLE
        if used > limit: return QuotaState.EXCEEDED
        if used == limit: return QuotaState.LIMITED
        return QuotaState.WARNING if used >= max(1, int(limit * .8)) else QuotaState.AVAILABLE
    def consume(self, organization_id: str, resource: str, quantity: int = 1) -> QuotaState:
        if quantity < 0: raise ValueError("quantity must be non-negative")
        limit, used = self.limits.get(resource), self.used.get((organization_id, resource), 0)
        if limit is not None and used + quantity > limit: return QuotaState.EXCEEDED
        self.used[(organization_id, resource)] = used + quantity
        return self.state(organization_id, resource)

class UsageMeter:
    def __init__(self): self.events: list[UsageEvent] = []
    def record(self, organization_id: str, resource_type: str, quantity: int = 1, employee_id: str | None = None, task_id: str | None = None) -> UsageEvent:
        raw = f"{organization_id}|{employee_id}|{task_id}|{resource_type}|{quantity}|{len(self.events)}".encode()
        event = UsageEvent(sha256(raw).hexdigest()[:16], organization_id, employee_id, task_id, resource_type, quantity, time()); self.events.append(event); return event
    def total(self, organization_id: str, resource_type: str) -> int: return sum(e.quantity for e in self.events if e.organization_id == organization_id and e.resource_type == resource_type)

class BillingProvider:
    configured = False
    def create_subscription(self, organization_id: str, package_id: str) -> BillingStatus: return BillingStatus.NOT_CONFIGURED
    def cancel_subscription(self, billing_reference: str) -> BillingStatus: return BillingStatus.NOT_CONFIGURED
    def verify_webhook(self, payload: bytes, signature: str, secret: str | None) -> bool:
        if not secret: return False
        return compare_digest(sha256(secret.encode() + payload).hexdigest(), signature)

class ServiceEngine:
    def __init__(self, store: TenantStore | None = None, billing: BillingProvider | None = None):
        self.store = store or TenantStore(); self.billing = billing or BillingProvider(); self.packages = PackageEngine(); self.subscriptions: dict[str, Subscription] = {}; self.contracts: dict[str, EmployeeContract] = {}; self.usage = UsageMeter(); self.quota = QuotaEngine({"tasks": 100, "messages": 500, "content": 100, "posts": 20, "employees": 2, "storage": 1000, "integrations": 2}); self.audit: list[AuditEvent] = []; self._idempotency: set[str] = set(); self._retention: dict[str, str] = {}
    def _audit(self, organization_id: str, actor: str, action: str, result: str, reference: str | None = None) -> None:
        raw = f"{organization_id}|{actor}|{action}|{result}|{reference}|{len(self.audit)}".encode(); self.audit.append(AuditEvent(sha256(raw).hexdigest()[:16], organization_id, actor, action, result, time(), reference))
    def create_organization(self, customer_id: str, organization_id: str) -> dict[str, Any]:
        self.store.organizations[organization_id] = {"customer_id": customer_id, "status": "ACTIVE"}; self._audit(organization_id, customer_id, "organization_created", "ACTIVE"); return dict(self.store.organizations[organization_id])
    def start_trial(self, organization_id: str, package_id: str = "FREE", *, idempotency_key: str | None = None) -> Subscription:
        if idempotency_key and idempotency_key in self._idempotency: return next(s for s in self.subscriptions.values() if s.organization_id == organization_id)
        self.packages.get(package_id); now = time(); sub = Subscription(f"sub_{len(self.subscriptions)+1}", organization_id, package_id, SubscriptionStatus.TRIAL, now, trial_end_at=now + 14 * 86400); self.subscriptions[sub.subscription_id] = sub
        if idempotency_key: self._idempotency.add(idempotency_key)
        self._audit(organization_id, "system", "subscription_created", sub.status.value, sub.subscription_id); return sub
    def activate_subscription(self, subscription_id: str, *, payment_authorized: bool, idempotency_key: str | None = None) -> Subscription:
        sub = self.subscriptions[subscription_id]
        if idempotency_key and idempotency_key in self._idempotency: return sub
        if not payment_authorized: raise PermissionError("PAYMENT_AUTHORIZATION_REQUIRED")
        if self.billing.create_subscription(sub.organization_id, sub.package_id) != BillingStatus.ACTIVE: raise RuntimeError(BillingStatus.NOT_CONFIGURED.value)
        updated = Subscription(sub.subscription_id, sub.organization_id, sub.package_id, SubscriptionStatus.ACTIVE, sub.start_at, sub.renew_at, sub.cancel_at, sub.trial_end_at, "configured"); self.subscriptions[subscription_id] = updated
        if idempotency_key: self._idempotency.add(idempotency_key)
        self._audit(sub.organization_id, "customer", "subscription_changed", "ACTIVE", subscription_id); return updated
    def change_package(self, subscription_id: str, package_id: str, *, authorized: bool, idempotency_key: str | None = None) -> Subscription:
        if not authorized: raise PermissionError("PACKAGE_CHANGE_NOT_AUTHORIZED")
        old = self.subscriptions[subscription_id]; self.packages.get(package_id); count = sum(1 for c in self.contracts.values() if c.organization_id == old.organization_id and c.status in {EmployeeContractStatus.ACTIVE, EmployeeContractStatus.TRIAL}); limit = self.packages.get(package_id).employee_limit
        if limit is not None and count > limit: raise ValueError("DOWNGRADE_BLOCKED_EMPLOYEE_LIMIT")
        updated = Subscription(old.subscription_id, old.organization_id, package_id, old.status, old.start_at, old.renew_at, old.cancel_at, old.trial_end_at, old.billing_reference); self.subscriptions[subscription_id] = updated
        if idempotency_key: self._idempotency.add(idempotency_key)
        self._audit(old.organization_id, "customer", "package_changed", package_id, subscription_id); return updated
    def cancel(self, subscription_id: str, *, immediate: bool, authorized: bool) -> Subscription:
        if not authorized: raise PermissionError("CANCELLATION_NOT_AUTHORIZED")
        old = self.subscriptions[subscription_id]; status = SubscriptionStatus.CANCELED if immediate else old.status; updated = Subscription(old.subscription_id, old.organization_id, old.package_id, status, old.start_at, old.renew_at, time() if immediate else old.cancel_at, old.trial_end_at, old.billing_reference); self.subscriptions[subscription_id] = updated; self._retention[old.organization_id] = "RETENTION"; self._audit(old.organization_id, "customer", "cancellation", status.value, subscription_id); return updated
    def hire_employee(self, organization_id: str, employee_kind: str, *, permissions: frozenset[str], configuration: Mapping[str, Any] | None = None) -> EmployeeContract:
        sub = next((s for s in self.subscriptions.values() if s.organization_id == organization_id and s.status in {SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE}), None)
        if not sub: raise PermissionError("NO_ACTIVE_SUBSCRIPTION")
        count = sum(1 for c in self.contracts.values() if c.organization_id == organization_id and c.status in {EmployeeContractStatus.TRIAL, EmployeeContractStatus.ACTIVE})
        if not self.packages.can_hire(sub.package_id, employee_kind, count): raise PermissionError("EMPLOYEE_ENTITLEMENT_DENIED")
        item = CATALOG[employee_kind]
        if not item.required_permissions.issubset(permissions): raise PermissionError("REQUIRED_PERMISSIONS_MISSING")
        employee_id = f"{organization_id}:{employee_kind}:{count+1}"; self.store.add_employee(Employee(employee_id, organization_id, item.role, permissions, EmployeeStatus.CONFIGURED)); status = EmployeeContractStatus.TRIAL if sub.status == SubscriptionStatus.TRIAL else EmployeeContractStatus.ACTIVE
        contract = EmployeeContract(f"contract_{len(self.contracts)+1}", employee_id, organization_id, sub.package_id, time(), sub.renew_at, permissions, {"tasks": self.quota.limits["tasks"]}, status, dict(configuration or {})); self.contracts[contract.contract_id] = contract; self._audit(organization_id, "customer", "employee_hired", status.value, contract.contract_id); return contract
    def record_usage(self, organization_id: str, resource: str, quantity: int = 1, *, employee_id: str | None = None, task_id: str | None = None) -> QuotaState:
        state = self.quota.consume(organization_id, resource, quantity)
        if state == QuotaState.EXCEEDED: self._audit(organization_id, "system", "quota_reached", state.value, resource); return state
        self.usage.record(organization_id, resource, quantity, employee_id, task_id)
        if state == QuotaState.WARNING: self._audit(organization_id, "system", "quota_warning", state.value, resource)
        return state
    def dashboard(self, organization_id: str) -> dict[str, Any]:
        if organization_id not in self.store.organizations: raise PermissionError("TENANT_NOT_FOUND")
        employees = [c for c in self.contracts.values() if c.organization_id == organization_id]; subs = [s for s in self.subscriptions.values() if s.organization_id == organization_id]
        return {"organization_id": organization_id, "employees": [c.employee_id for c in employees], "subscription": subs[-1].package_id if subs else "NO_DATA", "usage": {r: self.usage.total(organization_id, r) for r in self.quota.limits}, "quota": {r: self.quota.state(organization_id, r).value for r in self.quota.limits}, "billing_status": BillingStatus.ACTIVE.value if self.billing.configured else BillingStatus.NOT_CONFIGURED.value}
    def readiness(self, *, phase44_ready: bool, social_configured: bool, billing_configured: bool, validation_passed: bool = False, customer_surface_configured: bool = False) -> dict[str, Any]:
        base = {"employee_deployment": phase44_ready, "tenant_isolation": phase44_ready, "task_execution": phase44_ready, "verification": phase44_ready, "quota": True, "usage_metering": True, "subscription_state": True, "entitlement": True, "security": True, "audit": True, "customer_dashboard": customer_surface_configured, "employee_management": customer_surface_configured, "validation": validation_passed}
        free_ready = all(base.values())
        paid_ready = free_ready and social_configured and billing_configured
        return {"FREE_COMMERCIAL_READY": free_ready, "STARTER_199_COMMERCIAL_READY": paid_ready, "TEAM_399_COMMERCIAL_READY": paid_ready, "DEPARTMENT_699_COMMERCIAL_READY": paid_ready, "ORGANIZATION_1499_COMMERCIAL_READY": False, "evidence": base, "billing": BillingStatus.ACTIVE.value if billing_configured else BillingStatus.NOT_CONFIGURED.value}
