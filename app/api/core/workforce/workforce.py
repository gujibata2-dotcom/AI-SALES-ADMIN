"""Phase 46 multi-agent workforce orchestration.

Provider-neutral orchestration primitives. This module reuses the Phase 45 package
catalog and the Phase 42 organizational primitives; it never claims external model
execution or tool connectivity that has not been supplied by a real adapter.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from time import time
from typing import Any, Mapping

from app.api.core.service.service import PACKAGES
from app.api.core.organization.phase42 import external_content_as_data


class WorkforceStatus(str, Enum): DRAFT="DRAFT"; ACTIVE="ACTIVE"; PAUSED="PAUSED"; SUSPENDED="SUSPENDED"; RETIRED="RETIRED"
class EmployeeHealth(str, Enum): HEALTHY="HEALTHY"; DEGRADED="DEGRADED"; FAILED="FAILED"; UNAVAILABLE="UNAVAILABLE"
class MatchResult(str, Enum): EXACT_MATCH="EXACT_MATCH"; PARTIAL_MATCH="PARTIAL_MATCH"; NO_MATCH="NO_MATCH"
class TaskPriority(str, Enum): CRITICAL="CRITICAL"; HIGH="HIGH"; NORMAL="NORMAL"; LOW="LOW"
class TaskStatus(str, Enum): PLANNED="PLANNED"; READY="READY"; RUNNING="RUNNING"; BLOCKED="BLOCKED"; REVIEW="REVIEW"; COMPLETED="COMPLETED"; FAILED="FAILED"; REQUIRES_HUMAN="REQUIRES_HUMAN"; UNKNOWN="UNKNOWN"
class ReviewStatus(str, Enum): PENDING="PENDING"; APPROVED="APPROVED"; REVISE="REVISE"; REJECTED="REJECTED"; REVIEW_REQUIRED="REVIEW_REQUIRED"
class MemoryScope(str, Enum): PRIVATE="PRIVATE"; TEAM="TEAM"; ORGANIZATION="ORGANIZATION"; RESTRICTED="RESTRICTED"
class AutonomyLevel(str, Enum): L0="L0"; L1="L1"; L2="L2"; L3="L3"; L4="L4"

PACKAGE_EMPLOYEE_LIMITS = {k: v.employee_limit for k, v in PACKAGES.items()}
HIGH_RISK_ACTIONS = frozenset({"financial_action", "legal_commitment", "policy_change", "credential_change", "destructive_action", "high_impact_customer_action"})
UNTRUSTED_SOURCES = frozenset({"employee", "customer", "product", "web", "email", "document"})

@dataclass(frozen=True)
class Workforce:
    organization_id: str; workforce_id: str; package_id: str
    employees: tuple[str, ...] = (); departments: tuple[str, ...] = (); roles: tuple[str, ...] = ()
    policies: tuple[str, ...] = (); shared_goals: tuple[str, ...] = (); permissions: frozenset[str] = frozenset(); status: WorkforceStatus = WorkforceStatus.DRAFT

@dataclass
class WorkforceEmployee:
    employee_id: str; organization_id: str; workforce_id: str; role: str
    skills: frozenset[str]; knowledge_scopes: frozenset[str] = frozenset(); tools: frozenset[str] = frozenset()
    permissions: frozenset[str] = frozenset(); objectives: tuple[str, ...] = (); memory_scope: MemoryScope = MemoryScope.PRIVATE
    health: EmployeeHealth = EmployeeHealth.HEALTHY; workload: int = 0; capacity: int = 1; model_profile: str | None = None

@dataclass(frozen=True)
class Capability:
    capability_id: str; employee_id: str; organization_id: str; skill: str; level: str; domain: str
    tools: frozenset[str] = frozenset(); limitations: frozenset[str] = frozenset(); confidence: float = 0.0; evidence: tuple[str, ...] = ()

@dataclass
class WorkforceTask:
    task_id: str; organization_id: str; workforce_id: str; title: str; objective: str
    required_skills: frozenset[str] = frozenset(); required_knowledge: frozenset[str] = frozenset()
    risk: str = "UNKNOWN"; priority: TaskPriority = TaskPriority.NORMAL; deadline: str | None = None
    dependencies: tuple[str, ...] = (); assigned_employee: str | None = None; executing_employee: str | None = None
    reviewer: str | None = None; approver: str | None = None; status: TaskStatus = TaskStatus.PLANNED
    idempotency_key: str | None = None; result: Any = None; verification: str = "UNKNOWN"

@dataclass(frozen=True)
class EmployeeMessage:
    message_id: str; organization_id: str; workforce_id: str; task_id: str; sender: str; receiver: str
    message_type: str; context: Mapping[str, Any]; payload: Any; provenance: tuple[str, ...]; timestamp: float

@dataclass(frozen=True)
class Handoff:
    handoff_id: str; organization_id: str; workforce_id: str; task_id: str; sender: str; receiver: str
    context: Any; objective: str; completed_work: Any; remaining_work: Any; evidence: tuple[str, ...]
    limitations: tuple[str, ...]; risk: str; next_action: str

@dataclass(frozen=True)
class Review:
    review_id: str; organization_id: str; task_id: str; creator: str; reviewer: str
    status: ReviewStatus; evidence: tuple[str, ...]; confidence: float; findings: tuple[str, ...] = ()

@dataclass(frozen=True)
class WorkforcePolicy:
    organization_id: str; workforce_id: str; allowed_delegations: frozenset[str] = frozenset()
    review_roles: frozenset[str] = frozenset(); approval_roles: frozenset[str] = frozenset()
    allowed_tools: frozenset[str] = frozenset(); allowed_data_scopes: frozenset[str] = frozenset()
    allowed_actions: frozenset[str] = frozenset(); max_autonomy: AutonomyLevel = AutonomyLevel.L1
    high_risk_requires_human: bool = True

@dataclass
class Budget:
    task: float | None = None; employee: float | None = None; organization: float | None = None
    task_used: float = 0.0; employee_used: float = 0.0; organization_used: float = 0.0

@dataclass(frozen=True)
class WorkflowVersion:
    workflow_id: str; version: int; organization_id: str; created_at: float; author: str; reason: str; changes: tuple[str, ...]; status: str

@dataclass(frozen=True)
class WorkforceEvent:
    event_id: str; organization_id: str; workforce_id: str; task_id: str | None; employee_id: str | None
    action: str; tool: str | None; model: str | None; decision: str | None; approval: str | None
    result: str; verification: str; timestamp: float

class WorkforceEngine:
    """In-memory, deterministic control plane for Phase 46."""
    def __init__(self) -> None:
        self.workforces: dict[str, Workforce] = {}
        self.employees: dict[str, WorkforceEmployee] = {}
        self.capabilities: dict[str, Capability] = {}
        self.tasks: dict[str, WorkforceTask] = {}
        self.messages: list[EmployeeMessage] = []
        self.handoffs: list[Handoff] = []
        self.reviews: list[Review] = []
        self.policies: dict[str, WorkforcePolicy] = {}
        self.budgets: dict[str, Budget] = {}
        self.versions: dict[str, list[WorkflowVersion]] = {}
        self.events: list[WorkforceEvent] = []
        self.learning_events: list[Mapping[str, Any]] = []
        self.stopped_workforces: set[str] = set(); self.stopped_employees: set[str] = set(); self.stopped_tasks: set[str] = set(); self.stopped_tools: set[str] = set(); self.stopped_workflows: set[str] = set()
        self._idempotency: set[str] = set()

    def _event(self, org: str, wf: str, action: str, result: str, task: str | None = None, employee: str | None = None, **kw: Any) -> None:
        raw = f"{org}|{wf}|{task}|{employee}|{action}|{len(self.events)}".encode()
        self.events.append(WorkforceEvent(sha256(raw).hexdigest()[:16], org, wf, task, employee, action, kw.get("tool"), kw.get("model"), kw.get("decision"), kw.get("approval"), result, kw.get("verification", "UNKNOWN"), time()))

    def _tenant(self, organization_id: str, *objects: Any) -> None:
        for obj in objects:
            if getattr(obj, "organization_id", organization_id) != organization_id: raise PermissionError("DENY: cross-tenant access")

    def create_workforce(self, organization_id: str, workforce_id: str, package_id: str, goals: tuple[str, ...] = ()) -> Workforce:
        if package_id not in PACKAGES: raise ValueError("unknown package")
        key = f"{organization_id}:{workforce_id}"
        if key in self.workforces: raise ValueError("duplicate workforce")
        wf = Workforce(organization_id, workforce_id, package_id, shared_goals=goals)
        self.workforces[key] = wf; self.versions[workforce_id] = []
        self._event(organization_id, workforce_id, "workforce_created", "CREATED")
        return wf

    def set_policy(self, policy: WorkforcePolicy) -> None:
        self._tenant(policy.organization_id, policy); self.policies[policy.workforce_id] = policy

    def activate_workforce(self, organization_id: str, workforce_id: str) -> Workforce:
        wf = self._get_wf(organization_id, workforce_id)
        if not wf.employees: raise ValueError("activation requires at least one employee")
        if workforce_id in self.stopped_workflows or workforce_id in self.stopped_workforces: raise PermissionError("BLOCK: emergency stop active")
        updated = Workforce(**{**wf.__dict__, "status": WorkforceStatus.ACTIVE}); self.workforces[f"{organization_id}:{workforce_id}"] = updated
        self._event(organization_id, workforce_id, "workforce_activated", "ACTIVE"); return updated

    def _get_wf(self, org: str, wf_id: str) -> Workforce:
        wf = self.workforces.get(f"{org}:{wf_id}")
        if not wf: raise KeyError("workforce not found")
        return wf

    def add_employee(self, employee: WorkforceEmployee) -> WorkforceEmployee:
        wf = self._get_wf(employee.organization_id, employee.workforce_id)
        limit = PACKAGE_EMPLOYEE_LIMITS[wf.package_id]
        if limit is not None and len(wf.employees) >= limit: raise PermissionError("DENIED: package employee entitlement exceeded")
        if employee.employee_id in self.employees: raise ValueError("duplicate employee")
        self.employees[employee.employee_id] = employee
        self.workforces[f"{employee.organization_id}:{employee.workforce_id}"] = Workforce(**{**wf.__dict__, "employees": wf.employees + (employee.employee_id,), "roles": tuple(sorted(set(wf.roles + (employee.role,))))})
        self._event(employee.organization_id, employee.workforce_id, "employee_added", "ADDED", employee=employee.employee_id)
        return employee

    def register_capability(self, capability: Capability) -> None:
        self._tenant(capability.organization_id, capability)
        if capability.employee_id not in self.employees: raise KeyError("employee not found")
        if capability.confidence < 0 or capability.confidence > 1: raise ValueError("confidence must be 0..1")
        self.capabilities[capability.capability_id] = capability

    def match_capability(self, task: WorkforceTask, employee: WorkforceEmployee) -> MatchResult:
        self._tenant(task.organization_id, employee)
        skills = {c.skill for c in self.capabilities.values() if c.employee_id == employee.employee_id and c.organization_id == employee.organization_id and c.evidence}
        if not task.required_skills: return MatchResult.EXACT_MATCH
        if task.required_skills <= skills: return MatchResult.EXACT_MATCH
        if skills & task.required_skills: return MatchResult.PARTIAL_MATCH
        return MatchResult.NO_MATCH

    def assign(self, task_id: str, employee_id: str, authorized: bool = True) -> WorkforceTask:
        task = self.tasks[task_id]; emp = self.employees[employee_id]; self._tenant(task.organization_id, emp)
        if not authorized: raise PermissionError("BLOCK: unauthorized delegation")
        if emp.health in {EmployeeHealth.FAILED, EmployeeHealth.UNAVAILABLE}: raise PermissionError("BLOCK: employee unavailable")
        if self.match_capability(task, emp) != MatchResult.EXACT_MATCH: raise ValueError("NO_CAPABLE_EMPLOYEE")
        task.assigned_employee = employee_id; task.status = TaskStatus.READY; emp.workload += 1
        self._event(task.organization_id, task.workforce_id, "task_assigned", "READY", task=task_id, employee=employee_id); return task

    def decompose_goal(self, organization_id: str, workforce_id: str, goal: str) -> tuple[WorkforceTask, ...]:
        wf = self._get_wf(organization_id, workforce_id)
        if wf.status not in {WorkforceStatus.DRAFT, WorkforceStatus.ACTIVE}: raise PermissionError("workforce unavailable")
        if any(x in goal.lower() for x in ("เปิดตัว", "launch", "new product", "สินค้าใหม่")):
            stages = (("research","Research"),("market","Market Analysis"),("product","Product Analysis"),("content","Content"),("sales","Sales Preparation"),("support","Customer Support Preparation"),("campaign","Campaign"),("analytics","Analytics"))
        else: stages = (("goal","Goal Execution"),)
        created=[]; previous: tuple[str, ...] = ()
        for key, title in stages:
            tid=f"{workforce_id}:{key}"; task=WorkforceTask(tid,organization_id,workforce_id,title,goal,dependencies=previous); self.tasks[tid]=task; created.append(task); previous=(tid,)
        self._event(organization_id, workforce_id, "goal_decomposed", "PLANNED"); return tuple(created)

    def validate_dependencies(self, task_id: str) -> bool:
        task=self.tasks[task_id]
        for dep in task.dependencies:
            if dep not in self.tasks: raise ValueError("missing dependency")
            if self.tasks[dep].status != TaskStatus.COMPLETED: return False
        return True

    def parallel_ready(self, task_ids: tuple[str, ...]) -> tuple[str, ...]:
        ready=[]
        for tid in task_ids:
            task=self.tasks[tid]
            if self.validate_dependencies(tid) and task.status in {TaskStatus.READY, TaskStatus.PLANNED}: ready.append(tid)
        return tuple(ready)

    def authorize_action(self, organization_id: str, workforce_id: str, action: str, employee_id: str, approved: bool = False) -> bool:
        policy=self.policies.get(workforce_id)
        if not policy or policy.organization_id != organization_id: raise PermissionError("DENY: missing workforce policy")
        emp=self.employees[employee_id]; self._tenant(organization_id, emp)
        if action not in policy.allowed_actions: return False
        if action in HIGH_RISK_ACTIONS and policy.high_risk_requires_human and not approved: return False
        return True

    def authorize_tool(self, organization_id: str, workforce_id: str, employee_id: str, tool: str, action: str, approved: bool = False) -> bool:
        policy=self.policies.get(workforce_id); emp=self.employees[employee_id]; self._tenant(organization_id, emp)
        if not policy or tool not in policy.allowed_tools or tool not in emp.tools or action not in emp.permissions: return False
        return self.authorize_action(organization_id, workforce_id, action, employee_id, approved)

    def execute(self, task_id: str, executor: str, action: str = "work", model: str | None = None, approval: bool = False) -> WorkforceTask:
        task=self.tasks[task_id]; emp=self.employees[executor]; self._tenant(task.organization_id, emp)
        if task_id in self.stopped_tasks or task.workforce_id in self.stopped_workforces or executor in self.stopped_employees: raise PermissionError("BLOCK: emergency stop active")
        if not self.validate_dependencies(task_id): task.status=TaskStatus.BLOCKED; raise RuntimeError("BLOCKED: dependency")
        if task.risk in {"HIGH","CRITICAL"} and not approval: task.status=TaskStatus.REQUIRES_HUMAN; self._event(task.organization_id,task.workforce_id,"high_risk_review","REQUIRES_HUMAN",task=task_id,employee=executor); raise PermissionError("REQUIRES_HUMAN")
        task.executing_employee=executor; task.status=TaskStatus.RUNNING
        self._event(task.organization_id,task.workforce_id,"task_execution_started","RUNNING",task=task_id,employee=executor,model=model)
        return task

    def verify(self, task_id: str, verified: bool, result: Any = None) -> WorkforceTask:
        task=self.tasks[task_id]
        if task.status != TaskStatus.RUNNING: raise ValueError("task is not running")
        task.result=result; task.verification="VERIFIED" if verified else "FAILED"
        task.status=TaskStatus.COMPLETED if verified else TaskStatus.FAILED
        if task.executing_employee and task.executing_employee in self.employees: self.employees[task.executing_employee].workload=max(0,self.employees[task.executing_employee].workload-1)
        self._event(task.organization_id,task.workforce_id,"task_verified","COMPLETED" if verified else "FAILED",task=task_id,employee=task.executing_employee,verification=task.verification)
        self.learning_events.append({"organization_id":task.organization_id,"workforce_id":task.workforce_id,"task_id":task_id,"outcome":"SUCCESS" if verified else "FAILURE"})
        return task

    def collaborate(self, message: EmployeeMessage) -> EmployeeMessage:
        sender=self.employees.get(message.sender); receiver=self.employees.get(message.receiver)
        if not sender or not receiver: raise KeyError("employee not found")
        self._tenant(message.organization_id, sender, receiver)
        if sender.workforce_id != receiver.workforce_id or message.workforce_id != sender.workforce_id: raise PermissionError("DENY: workforce boundary")
        self.messages.append(message); return message

    def handoff(self, handoff: Handoff) -> Handoff:
        s=self.employees[handoff.sender]; r=self.employees[handoff.receiver]; self._tenant(handoff.organization_id,s,r)
        if s.workforce_id != r.workforce_id: raise PermissionError("DENY: cross-workforce handoff")
        if not handoff.context or not handoff.objective or not handoff.next_action: raise ValueError("incomplete handoff context")
        self.handoffs.append(handoff); return handoff

    def review(self, task_id: str, reviewer: str, approved: bool, evidence: tuple[str, ...] = (), confidence: float = 0.0, findings: tuple[str, ...] = ()) -> Review:
        task=self.tasks[task_id]
        if reviewer == task.executing_employee: raise PermissionError("creator cannot be sole validator")
        if confidence < 0 or confidence > 1: raise ValueError("confidence must be 0..1")
        status=ReviewStatus.APPROVED if approved and evidence else ReviewStatus.REVISE
        review=Review(f"review:{task_id}:{len(self.reviews)}",task.organization_id,task_id,task.executing_employee or "UNKNOWN",reviewer,status,evidence,confidence,findings); self.reviews.append(review)
        task.reviewer=reviewer
        if status != ReviewStatus.APPROVED: task.status=TaskStatus.REVIEW
        return review

    def resolve_disagreement(self, task_id: str, outputs: tuple[Mapping[str, Any], ...]) -> Mapping[str, Any]:
        if len(outputs) < 2: raise ValueError("requires competing outputs")
        evidence=[x for x in outputs if x.get("evidence")]; ranked=sorted(evidence or outputs, key=lambda x: float(x.get("confidence",0)), reverse=True)
        top=ranked[0]
        if len(ranked)>1 and float(top.get("confidence",0)) == float(ranked[1].get("confidence",0)) and top.get("evidence") != ranked[1].get("evidence"): return {"status":"REQUIRES_HUMAN","reason":"unresolved evidence conflict"}
        return {"status":"RESOLVED","source":top.get("source"),"evidence":top.get("evidence",()),"uncertainty":top.get("uncertainty"),"limitations":top.get("limitations",())}

    def synthesize(self, task_id: str, outputs: tuple[Mapping[str, Any], ...]) -> Mapping[str, Any]:
        if not outputs: return {"status":"REVIEW_REQUIRED"}
        result=self.resolve_disagreement(task_id, outputs)
        if result["status"] == "REQUIRES_HUMAN": return result
        return {**result,"sources":tuple(x.get("source") for x in outputs if x.get("source")),"verification":"REVIEW_REQUIRED"}

    def quality_gate(self, task_id: str, accuracy: bool, completeness: bool, consistency: bool, evidence: bool, risk_ok: bool, policy_ok: bool, verification: bool) -> str:
        status="PASS" if all((accuracy,completeness,consistency,evidence,risk_ok,policy_ok,verification)) else "REVIEW_REQUIRED"
        self._event(self.tasks[task_id].organization_id,self.tasks[task_id].workforce_id,"quality_gate",status,task=task_id,verification="VERIFIED" if verification else "UNKNOWN")
        return status

    def consume_budget(self, organization_id: str, workforce_id: str, amount: float, employee_id: str | None = None, task_id: str | None = None) -> str:
        b=self.budgets.setdefault(workforce_id,Budget()); b.organization_id = organization_id if hasattr(b,"organization_id") else organization_id
        if amount < 0: raise ValueError("amount must be non-negative")
        if b.organization is not None and b.organization_used + amount > b.organization: return "PAUSE"
        if b.employee is not None and employee_id and b.employee_used + amount > b.employee: return "PAUSE"
        if b.task is not None and task_id and b.task_used + amount > b.task: return "PAUSE"
        b.organization_used += amount
        if employee_id: b.employee_used += amount
        if task_id: b.task_used += amount
        limits=(b.organization,b.employee,b.task); used=(b.organization_used,b.employee_used,b.task_used)
        return "WARNING" if any(l is not None and u >= .8*l for l,u in zip(limits,used)) else "AVAILABLE"

    def stop(self, scope: str, identifier: str) -> None:
        {"WORKFORCE":self.stopped_workforces,"EMPLOYEE":self.stopped_employees,"TASK":self.stopped_tasks,"TOOL":self.stopped_tools,"WORKFLOW":self.stopped_workflows}[scope].add(identifier)

    def recover(self, task_id: str, safe_retry: bool, fallback_employee: str | None = None) -> str:
        task=self.tasks[task_id]
        if safe_retry: task.status=TaskStatus.READY; return "RETRY"
        if fallback_employee:
            self.assign(task_id,fallback_employee); return "REASSIGN"
        task.status=TaskStatus.REQUIRES_HUMAN; return "HUMAN_ESCALATION"

    def route_model(self, requirements: Mapping[str, Any], models: tuple[Mapping[str, Any], ...]) -> Mapping[str, Any] | None:
        candidates=[m for m in models if m.get("available") and set(requirements.get("capabilities",())) <= set(m.get("capabilities",()))]
        if not candidates: return None
        return sorted(candidates,key=lambda m:(float(m.get("quality",0)), -float(m.get("cost",0))),reverse=True)[0]

    def autonomy_allowed(self, policy: WorkforcePolicy, requested: AutonomyLevel) -> bool: return AutonomyLevel(list(AutonomyLevel).index(requested)) <= policy.max_autonomy if False else list(AutonomyLevel).index(requested) <= list(AutonomyLevel).index(policy.max_autonomy)

    def external_input(self, source: str, content: Any) -> Mapping[str, Any]:
        if source.lower() not in UNTRUSTED_SOURCES: raise ValueError("unknown external source")
        return external_content_as_data(content)

    def record_learning(self, organization_id: str, workforce_id: str, task_id: str, feedback: Mapping[str, Any]) -> Mapping[str, Any]:
        event={"organization_id":organization_id,"workforce_id":workforce_id,"task_id":task_id,"feedback":dict(feedback),"provenance":"PHASE46"}; self.learning_events.append(event); return event

    def dashboard(self, organization_id: str, workforce_id: str) -> Mapping[str, Any]:
        wf=self._get_wf(organization_id,workforce_id); employees=[e for e in self.employees.values() if e.organization_id==organization_id and e.workforce_id==workforce_id]; tasks=[t for t in self.tasks.values() if t.organization_id==organization_id and t.workforce_id==workforce_id]
        return {"workforce":wf,"employees":tuple(employees),"tasks":tuple(tasks),"running":sum(t.status==TaskStatus.RUNNING for t in tasks),"completed":sum(t.status==TaskStatus.COMPLETED for t in tasks),"failed":sum(t.status==TaskStatus.FAILED for t in tasks),"review":sum(t.status in {TaskStatus.REVIEW,TaskStatus.REQUIRES_HUMAN} for t in tasks),"outcomes":tuple(e for e in self.learning_events if e.get("organization_id")==organization_id and e.get("workforce_id")==workforce_id)}

__all__=["WorkforceEngine","Workforce","WorkforceEmployee","Capability","WorkforceTask","EmployeeMessage","Handoff","Review","WorkforcePolicy","Budget","WorkflowVersion","WorkforceStatus","EmployeeHealth","MatchResult","TaskPriority","TaskStatus","ReviewStatus","MemoryScope","AutonomyLevel"]
