"""Phase 46 AI Employee Multi-Agent Team & Workforce Orchestration Engine.

Stdlib-only coordination layer. It plans, authorizes, delegates, reviews and
synthesizes work but never invents provider/model execution or publication.
Execution is delegated to the existing Phase 44 runtime when supplied.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from time import time
from typing import Any, Callable, Mapping, Sequence

from app.api.core.production.runtime import Employee as RuntimeEmployee
from app.api.core.production.runtime import EmployeeStatus, EmployeeRuntime, Task as RuntimeTask
from app.api.core.service.service import ServiceEngine


class WorkforceStatus(str, Enum):
    DRAFT = "DRAFT"; ACTIVE = "ACTIVE"; PAUSED = "PAUSED"; SUSPENDED = "SUSPENDED"; RETIRED = "RETIRED"
class EmployeeHealth(str, Enum): HEALTHY = "HEALTHY"; DEGRADED = "DEGRADED"; FAILED = "FAILED"; UNAVAILABLE = "UNAVAILABLE"
class TaskPriority(str, Enum): CRITICAL = "CRITICAL"; HIGH = "HIGH"; NORMAL = "NORMAL"; LOW = "LOW"
class MatchType(str, Enum): EXACT_MATCH = "EXACT_MATCH"; PARTIAL_MATCH = "PARTIAL_MATCH"; NO_MATCH = "NO_MATCH"
class ReviewStatus(str, Enum): PENDING = "PENDING"; APPROVED = "APPROVED"; REVISE = "REVISE"; ESCALATED = "ESCALATED"
class AutonomyLevel(str, Enum): L0 = "L0_HUMAN_ONLY"; L1 = "L1_AI_ASSIST"; L2 = "L2_AI_EXECUTE_HUMAN_APPROVAL"; L3 = "L3_AI_EXCEPTION_ESCALATION"; L4 = "L4_HIGH_AUTONOMY"

HIGH_RISK_ACTIONS = frozenset({"financial_action", "legal_commitment", "policy_change", "credential_change", "destructive_action", "high_impact_customer_action"})

@dataclass(frozen=True)
class Workforce:
    organization_id: str
    workforce_id: str
    employees: tuple[str, ...] = ()
    departments: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()
    policies: tuple[str, ...] = ()
    shared_goals: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
    status: WorkforceStatus = WorkforceStatus.DRAFT
    version: int = 1

@dataclass(frozen=True)
class Capability:
    capability_id: str
    employee_id: str
    skill: str
    level: str
    domain: str
    tools: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    confidence: str = "UNKNOWN"
    evidence: tuple[str, ...] = ()

@dataclass(frozen=True)
class WorkforceTask:
    task_id: str
    organization_id: str
    title: str
    objective: str
    required_skills: tuple[str, ...] = ()
    required_knowledge: tuple[str, ...] = ()
    risk: str = "UNKNOWN"
    priority: TaskPriority = TaskPriority.NORMAL
    dependencies: tuple[str, ...] = ()
    assigned_employee: str | None = None
    status: str = "PENDING"
    idempotency_key: str | None = None
    version: int = 1

@dataclass(frozen=True)
class Assignment:
    assignment_id: str
    task_id: str
    employee_id: str | None
    match: MatchType
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]
    confidence: str
    rationale: str

@dataclass(frozen=True)
class AgentMessage:
    message_id: str
    organization_id: str
    sender: str
    receiver: str
    task_id: str
    message_type: str
    payload: Mapping[str, Any]
    provenance: tuple[str, ...]
    timestamp: float

@dataclass(frozen=True)
class Handoff:
    handoff_id: str
    organization_id: str
    task_id: str
    sender: str
    receiver: str
    context: Mapping[str, Any]
    objective: str
    completed_work: tuple[str, ...]
    remaining_work: tuple[str, ...]
    evidence: tuple[str, ...]
    limitations: tuple[str, ...]
    risk: str
    next_action: str
    verified: bool = False

@dataclass(frozen=True)
class Review:
    review_id: str
    organization_id: str
    task_id: str
    creator: str
    reviewer: str
    status: ReviewStatus
    evidence: tuple[str, ...] = ()
    findings: tuple[str, ...] = ()
    confidence: str = "UNKNOWN"

@dataclass(frozen=True)
class WorkforcePolicy:
    policy_id: str
    organization_id: str
    max_autonomy: AutonomyLevel = AutonomyLevel.L2
    high_risk_requires_human: bool = True
    allowed_tools: frozenset[str] = frozenset()
    allowed_actions: frozenset[str] = frozenset()
    reviewers: frozenset[str] = frozenset()
    approvers: frozenset[str] = frozenset()

@dataclass(frozen=True)
class Budget:
    task_limit: float | None = None
    employee_limit: float | None = None
    organization_limit: float | None = None
    task_spend: Mapping[str, float] = field(default_factory=dict)
    employee_spend: Mapping[str, float] = field(default_factory=dict)
    organization_spend: float = 0.0

@dataclass(frozen=True)
class WorkforceEvent:
    event_id: str
    organization_id: str
    workforce_id: str
    task_id: str | None
    employee_id: str | None
    action: str
    result: str
    authorization: str
    timestamp: float

@dataclass(frozen=True)
class Outcome:
    task_id: str
    status: str
    output: Any
    verified: bool
    evidence: tuple[str, ...] = ()
    uncertainty: str = "UNKNOWN"
    limitations: tuple[str, ...] = ()


class WorkforceEngine:
    """Tenant-bound orchestrator; execution remains a Phase 44 runtime concern."""
    def __init__(self, service: ServiceEngine | None = None) -> None:
        self.service = service or ServiceEngine()
        self.workforces: dict[str, Workforce] = {}
        self.capabilities: dict[str, Capability] = {}
        self.tasks: dict[str, WorkforceTask] = {}
        self.messages: list[AgentMessage] = []
        self.handoffs: list[Handoff] = []
        self.reviews: list[Review] = []
        self.policies: dict[str, WorkforcePolicy] = {}
        self.health: dict[str, EmployeeHealth] = {}
        self.budgets: dict[str, Budget] = {}
        self.events: list[WorkforceEvent] = []
        self.learning_events: list[dict[str, Any]] = []
        self._stopped: set[tuple[str, str]] = set()
        self._idempotency: set[str] = set()

    def _tenant(self, organization_id: str) -> None:
        if organization_id not in self.service.store.organizations:
            raise PermissionError("TENANT_NOT_FOUND")

    def _event(self, organization_id: str, workforce_id: str, action: str, result: str, *, task_id: str | None = None, employee_id: str | None = None, authorization: str = "SYSTEM") -> None:
        raw = f"{organization_id}|{workforce_id}|{task_id}|{employee_id}|{action}|{len(self.events)}".encode()
        self.events.append(WorkforceEvent(sha256(raw).hexdigest()[:16], organization_id, workforce_id, task_id, employee_id, action, result, authorization, time()))

    def create_workforce(self, organization_id: str, workforce_id: str, *, policy: WorkforcePolicy | None = None) -> Workforce:
        self._tenant(organization_id)
        if workforce_id in self.workforces: raise ValueError("DUPLICATE_WORKFORCE")
        wf = Workforce(organization_id, workforce_id)
        self.workforces[workforce_id] = wf
        if policy: self.policies[workforce_id] = policy
        self._event(organization_id, workforce_id, "WORKFORCE_CREATE", "DRAFT")
        return wf

    def activate_workforce(self, workforce_id: str) -> Workforce:
        wf = self.workforces[workforce_id]
        if not wf.employees: raise PermissionError("ACTIVATION_REQUIRES_EMPLOYEE")
        policy = self.policies.get(workforce_id)
        if policy and policy.max_autonomy == AutonomyLevel.L4 and not policy.approvers:
            raise PermissionError("L4_REQUIRES_APPROVER_POLICY")
        updated = Workforce(**{**wf.__dict__, "status": WorkforceStatus.ACTIVE})
        self.workforces[workforce_id] = updated
        self._event(wf.organization_id, workforce_id, "WORKFORCE_ACTIVATE", "ACTIVE")
        return updated

    def add_employee(self, workforce_id: str, employee_id: str) -> Workforce:
        wf = self.workforces[workforce_id]
        self._tenant(wf.organization_id)
        employee = self.service.store.get_employee(wf.organization_id, employee_id)
        if employee.status not in {EmployeeStatus.ACTIVE, EmployeeStatus.CONFIGURED}:
            raise PermissionError("EMPLOYEE_NOT_DEPLOYABLE")
        if employee_id not in [c.employee_id for c in self.service.contracts.values() if c.organization_id == wf.organization_id]:
            raise PermissionError("EMPLOYEE_CONTRACT_NOT_FOUND")
        package = next((s.package_id for s in self.service.subscriptions.values() if s.organization_id == wf.organization_id and s.status.value in {"TRIAL", "ACTIVE"}), None)
        if package is None: raise PermissionError("NO_ACTIVE_SUBSCRIPTION")
        entitled = self.service.packages.get(package).employee_limit
        if entitled is not None and len(wf.employees) >= entitled: raise PermissionError("EMPLOYEE_ENTITLEMENT_DENIED")
        employees = tuple(dict.fromkeys((*wf.employees, employee_id)))
        updated = Workforce(**{**wf.__dict__, "employees": employees})
        self.workforces[workforce_id] = updated
        self._event(wf.organization_id, workforce_id, "EMPLOYEE_ASSIGN_TO_WORKFORCE", "ASSIGNED", employee_id=employee_id)
        return updated

    def register_capability(self, capability: Capability) -> None:
        wf = self.workforces[next(k for k,v in self.workforces.items() if v.organization_id == self.service.store.employees[capability.employee_id].organization_id and capability.employee_id in v.employees)]
        if not capability.evidence: raise ValueError("CAPABILITY_REQUIRES_EVIDENCE")
        self.capabilities[capability.capability_id] = capability
        self._event(wf.organization_id, wf.workforce_id, "CAPABILITY_REGISTER", "EVIDENCE_BACKED", employee_id=capability.employee_id)

    def decompose_goal(self, organization_id: str, goal: str, *, task_prefix: str = "task") -> tuple[WorkforceTask, ...]:
        self._tenant(organization_id)
        normalized = goal.lower().strip()
        templates = {
            "เปิดตัวสินค้าใหม่": [("research", ("research",)), ("content", ("content",)), ("sales", ("sales",)), ("support", ("support",)), ("campaign", ("marketing",))],
            "launch new product": [("research", ("research",)), ("content", ("content",)), ("sales", ("sales",)), ("support", ("support",)), ("campaign", ("marketing",))],
        }
        selected = templates.get(normalized)
        if selected is None:
            return (WorkforceTask(f"{task_prefix}:1", organization_id, goal, goal, (), risk="UNKNOWN"),)
        tasks: list[WorkforceTask] = []
        previous: str | None = None
        for idx, (title, skills) in enumerate(selected, 1):
            tid = f"{task_prefix}:{idx}"
            tasks.append(WorkforceTask(tid, organization_id, title, title, skills, dependencies=(previous,) if previous and title in {"content", "sales", "support", "campaign"} else ()))
            previous = tid
        for task in tasks: self.tasks[task.task_id] = task
        return tuple(tasks)

    def match_capability(self, task: WorkforceTask) -> tuple[Assignment, ...]:
        self._tenant(task.organization_id)
        employees = [e for e in self.service.store.employees.values() if e.organization_id == task.organization_id]
        results: list[Assignment] = []
        for employee in employees:
            caps = [c for c in self.capabilities.values() if c.employee_id == employee.employee_id and c.confidence != "UNKNOWN"]
            skills = {c.skill for c in caps}
            matched = tuple(sorted(skills & set(task.required_skills)))
            missing = tuple(sorted(set(task.required_skills) - skills))
            if not matched: match = MatchType.NO_MATCH
            elif missing: match = MatchType.PARTIAL_MATCH
            else: match = MatchType.EXACT_MATCH
            results.append(Assignment(f"assign:{task.task_id}:{employee.employee_id}", task.task_id, employee.employee_id if match != MatchType.NO_MATCH else None, match, matched, missing, "KNOWN" if match == MatchType.EXACT_MATCH else "ESTIMATED", "evidence-backed capability match"))
        return tuple(sorted(results, key=lambda a: (a.match != MatchType.EXACT_MATCH, a.match == MatchType.NO_MATCH)))

    def assign(self, task_id: str) -> Assignment:
        task = self.tasks[task_id]
        candidates = self.match_capability(task)
        exact = next((a for a in candidates if a.match == MatchType.EXACT_MATCH), None)
        if exact is None: raise PermissionError("NO_CAPABLE_EMPLOYEE")
        updated = WorkforceTask(**{**task.__dict__, "assigned_employee": exact.employee_id, "status": "ASSIGNED"})
        self.tasks[task_id] = updated
        wf = next(w for w in self.workforces.values() if w.organization_id == task.organization_id)
        self._event(task.organization_id, wf.workforce_id, "TASK_ASSIGN", "ASSIGNED", task_id=task_id, employee_id=exact.employee_id)
        return exact

    def dependency_order(self, task_ids: Sequence[str]) -> tuple[str, ...]:
        selected = {tid: self.tasks[tid] for tid in task_ids}
        deps = {tid: set(t.dependencies) & set(selected) for tid,t in selected.items()}
        result: list[str] = []
        while deps:
            ready = sorted(tid for tid, values in deps.items() if not values)
            if not ready: raise ValueError("DEPENDENCY_CYCLE")
            result.extend(ready)
            for tid in ready: deps.pop(tid)
            for values in deps.values(): values.difference_update(ready)
        return tuple(result)

    def can_parallelize(self, task_ids: Sequence[str]) -> bool:
        selected = [self.tasks[tid] for tid in task_ids]
        return all(not t.dependencies for t in selected) and len({t.assigned_employee for t in selected}) == len(selected)

    def collaborate(self, message: AgentMessage) -> AgentMessage:
        self._tenant(message.organization_id)
        self.service.store.get_employee(message.organization_id, message.sender)
        self.service.store.get_employee(message.organization_id, message.receiver)
        if not message.provenance: raise PermissionError("MESSAGE_PROVENANCE_REQUIRED")
        self.messages.append(message)
        return message

    def handoff(self, handoff: Handoff) -> Handoff:
        self._tenant(handoff.organization_id)
        if handoff.sender == handoff.receiver: raise ValueError("CREATOR_CANNOT_BE_SOLE_REVIEWER")
        if not handoff.context or not handoff.objective or not handoff.next_action: raise ValueError("HANDOFF_CONTEXT_INCOMPLETE")
        self.service.store.get_employee(handoff.organization_id, handoff.sender)
        self.service.store.get_employee(handoff.organization_id, handoff.receiver)
        self.handoffs.append(handoff)
        return handoff

    def review(self, review: Review) -> Review:
        self._tenant(review.organization_id)
        if review.creator == review.reviewer: raise PermissionError("INDEPENDENT_REVIEW_REQUIRED")
        self.service.store.get_employee(review.organization_id, review.creator)
        self.service.store.get_employee(review.organization_id, review.reviewer)
        self.reviews.append(review)
        return review

    def resolve_disagreement(self, task_id: str, outputs: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
        if len(outputs) < 2: raise ValueError("DISAGREEMENT_REQUIRES_MULTIPLE_OUTPUTS")
        evidence = [o.get("evidence", ()) for o in outputs]
        verified = [bool(o.get("verified")) for o in outputs]
        if not all(verified): return {"status": "REVIEW_REQUIRED", "reason": "UNVERIFIED_OUTPUT"}
        scores = [len(e) for e in evidence]
        if len(set(scores)) == 1: return {"status": "REVIEW_REQUIRED", "reason": "CONFLICT_REQUIRES_HUMAN_REVIEW"}
        winner = outputs[scores.index(max(scores))]
        return {"status": "CANDIDATE", "task_id": task_id, "output": winner, "basis": "evidence_count_only; human/domain review may still be required"}

    def authorize_action(self, workforce_id: str, task_id: str, action: str, autonomy: AutonomyLevel, *, human_approved: bool = False) -> bool:
        wf = self.workforces[workforce_id]; policy = self.policies.get(workforce_id, WorkforcePolicy("default", wf.organization_id))
        if autonomy.value > policy.max_autonomy.value: raise PermissionError("AUTONOMY_EXCEEDS_POLICY")
        if action in HIGH_RISK_ACTIONS and policy.high_risk_requires_human and not human_approved: return False
        if policy.allowed_actions and action not in policy.allowed_actions: return False
        return True

    def record_cost(self, workforce_id: str, *, task_id: str, employee_id: str, amount: float) -> str:
        if amount < 0: raise ValueError("NEGATIVE_COST")
        budget = self.budgets.get(workforce_id, Budget())
        task_spend = dict(budget.task_spend); task_spend[task_id] = task_spend.get(task_id, 0.0) + amount
        employee_spend = dict(budget.employee_spend); employee_spend[employee_id] = employee_spend.get(employee_id, 0.0) + amount
        total = budget.organization_spend + amount
        status = "OK"
        if budget.task_limit is not None and task_spend[task_id] >= budget.task_limit: status = "PAUSE"
        if budget.employee_limit is not None and employee_spend[employee_id] >= budget.employee_limit: status = "PAUSE"
        if budget.organization_limit is not None and total >= budget.organization_limit: status = "PAUSE"
        self.budgets[workforce_id] = Budget(budget.task_limit, budget.employee_limit, budget.organization_limit, task_spend, employee_spend, total)
        return status

    def set_health(self, employee_id: str, health: EmployeeHealth) -> None: self.health[employee_id] = health

    def recover(self, task_id: str) -> str:
        task = self.tasks[task_id]
        if task.assigned_employee and self.health.get(task.assigned_employee, EmployeeHealth.HEALTHY) == EmployeeHealth.UNAVAILABLE:
            alternatives = [a for a in self.match_capability(task) if a.employee_id != task.assigned_employee and a.match == MatchType.EXACT_MATCH]
            if alternatives:
                self.tasks[task_id] = WorkforceTask(**{**task.__dict__, "assigned_employee": alternatives[0].employee_id, "status": "REASSIGNED"})
                return "REASSIGNED"
            return "ESCALATE"
        return "NO_RECOVERY_NEEDED"

    def execute(self, task_id: str, runtime: EmployeeRuntime, handler: Callable[[RuntimeTask], Any], verify: Callable[[Any], bool]) -> Any:
        task = self.tasks[task_id]
        if task.assigned_employee is None: raise PermissionError("TASK_NOT_ASSIGNED")
        if task.idempotency_key and task.idempotency_key in self._idempotency: return {"status": "DUPLICATE_PREVENTED"}
        if ("task", task_id) in self._stopped or ("employee", task.assigned_employee) in self._stopped: return {"status": "BLOCKED", "reason": "EMERGENCY_STOP"}
        rt = RuntimeTask(task.task_id, task.organization_id, task.assigned_employee, task.objective, task.objective, idempotency_key=task.idempotency_key)
        result = runtime.execute(rt, handler, verify=verify)
        if task.idempotency_key: self._idempotency.add(task.idempotency_key)
        self.learning_events.append({"task_id": task_id, "status": result.status.value, "verified": result.verified, "source": "PHASE_46"})
        return result

    def synthesize(self, task_id: str, outputs: Sequence[Mapping[str, Any]], *, verified: bool = False) -> Outcome:
        if not outputs: raise ValueError("NO_OUTPUTS")
        sources = tuple(str(o.get("source")) for o in outputs if o.get("source"))
        evidence = tuple(str(e) for o in outputs for e in o.get("evidence", ()) if e)
        uncertainty = "KNOWN" if verified and all(o.get("verified") for o in outputs) else "UNKNOWN"
        if not verified: return Outcome(task_id, "REVIEW_REQUIRED", outputs, False, evidence, uncertainty, ("final synthesis is not independently verified",))
        return Outcome(task_id, "CANDIDATE", {"sources": sources, "outputs": list(outputs)}, True, evidence, uncertainty)

    def stop(self, scope: str, identifier: str) -> None: self._stopped.add((scope, identifier))
    def is_stopped(self, scope: str, identifier: str) -> bool: return (scope, identifier) in self._stopped

    def external_content_as_data(self, content: Any) -> Mapping[str, Any]:
        return {"data": content, "instructions_trusted": False, "source": "EXTERNAL_UNTRUSTED"}

    def dashboard(self, organization_id: str) -> Mapping[str, Any]:
        self._tenant(organization_id)
        wfs = [w for w in self.workforces.values() if w.organization_id == organization_id]
        tasks = [t for t in self.tasks.values() if t.organization_id == organization_id]
        return {"workforces": wfs, "employees": [e for e in self.service.store.employees.values() if e.organization_id == organization_id], "tasks": tasks, "events": [e for e in self.events if e.organization_id == organization_id], "learning_events": [e for e in self.learning_events if self.tasks.get(e["task_id"]).organization_id == organization_id]}
