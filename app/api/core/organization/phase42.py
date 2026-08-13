"""Phase 42 organizational orchestration contracts and pure planning primitives.

Provider-neutral, standard-library only. Integrates with the existing Phase 30
organization and orchestration packages; it does not execute tools or agents.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

class TaskStatus(str, Enum):
    PENDING="PENDING"; PLANNED="PLANNED"; ASSIGNED="ASSIGNED"; IN_PROGRESS="IN_PROGRESS"; BLOCKED="BLOCKED"; REVIEW="REVIEW"; COMPLETED="COMPLETED"; FAILED="FAILED"; CANCELLED="CANCELLED"; ESCALATED="ESCALATED"
class QualityGate(str, Enum): PASS="PASS"; FAIL="FAIL"; REVIEW_REQUIRED="REVIEW_REQUIRED"; UNKNOWN="UNKNOWN"
class Authorization(str, Enum): AUTO_ALLOWED="AUTO_ALLOWED"; POLICY_ALLOWED="POLICY_ALLOWED"; HUMAN_APPROVAL_REQUIRED="HUMAN_APPROVAL_REQUIRED"; EXECUTIVE_APPROVAL_REQUIRED="EXECUTIVE_APPROVAL_REQUIRED"; PROHIBITED="PROHIBITED"

@dataclass(frozen=True)
class Capability:
    capability: str
    proficiency: str
    confidence: str
    evidence: tuple[str, ...] = ()
    last_evaluated: str | None = None
    limitations: tuple[str, ...] = ()
    def evidenced(self) -> bool: return bool(self.evidence)

@dataclass
class Employee:
    employee_id: str
    role: str
    capabilities: list[Capability]
    knowledge_scope: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    authority_level: str = "WORKER"
    constraints: tuple[str, ...] = ()
    availability: bool = True
    workload: int = 0
    capacity: int = 1
    reliability: str = "UNKNOWN"
    specializations: tuple[str, ...] = ()
    status: str = "ACTIVE"
    version: int = 1

@dataclass(frozen=True)
class Task:
    task_id: str
    title: str
    description: str
    objective: str
    required_capabilities: tuple[str, ...] = ()
    priority: str = "MEDIUM"
    risk: str = "UNKNOWN"
    deadline: str | None = None
    dependencies: tuple[str, ...] = ()
    parent_id: str | None = None
    assigned_employee: str | None = None
    status: TaskStatus = TaskStatus.PENDING

@dataclass(frozen=True)
class Assignment:
    assignment_id: str
    task_id: str
    employee_id: str
    capability_match: tuple[str, ...]
    capability_gap: tuple[str, ...]
    confidence: str
    rationale: str
    authorized: bool = False

@dataclass(frozen=True)
class AgentMessage:
    message_id: str
    sender: str
    receiver: str
    purpose: str
    context: Mapping[str, Any]
    data: Any
    authorization_scope: tuple[str, ...]
    timestamp: str
    authenticated: bool = False

@dataclass(frozen=True)
class Handoff:
    handoff_id: str
    task_id: str
    sender: str
    receiver: str
    input: Any
    output: Any
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    verification_status: str

@dataclass(frozen=True)
class OrganizationEvent:
    event_id: str
    task_id: str | None
    agent_id: str | None
    action: str
    reason: str
    timestamp: str
    authorization: str
    result: str

class Registry:
    def __init__(self): self.items: dict[str, Any] = {}
    def add(self, item: Any, key: str) -> None:
        if key in self.items: raise ValueError(f"duplicate registry id: {key}")
        self.items[key] = item
    def get(self, key: str) -> Any: return self.items.get(key)
    def values(self): return tuple(self.items.values())

def capability_match(task: Task, employee: Employee) -> Assignment:
    available = {c.capability for c in employee.capabilities if c.evidenced()}
    required = set(task.required_capabilities)
    matched, gap = required & available, required - available
    confidence = "UNKNOWN" if gap else ("ESTIMATED" if any(c.confidence != "KNOWN" for c in employee.capabilities if c.capability in matched) else "KNOWN")
    return Assignment(f"assign:{task.task_id}:{employee.employee_id}", task.task_id, employee.employee_id, tuple(sorted(matched)), tuple(sorted(gap)), confidence, "evidence-backed capability match" if not gap else "capability gap detected")

def select_employee(task: Task, employees: list[Employee]) -> list[Assignment]:
    candidates = [capability_match(task, e) for e in employees if e.status == "ACTIVE" and e.availability and e.workload < e.capacity]
    return sorted(candidates, key=lambda a: (bool(a.capability_gap), a.confidence != "KNOWN"))

def topological_order(tasks: list[Task]) -> tuple[str, ...]:
    ids = {t.task_id for t in tasks}; deps = {t.task_id: set(t.dependencies) & ids for t in tasks}; out=[]
    while deps:
        ready = sorted(k for k,v in deps.items() if not v)
        if not ready: raise ValueError("dependency cycle detected")
        out.extend(ready)
        for k in ready: deps.pop(k)
        for v in deps.values(): v.difference_update(ready)
    return tuple(out)

def critical_tasks(tasks: list[Task]) -> tuple[str, ...]:
    order = topological_order(tasks); downstream={t.task_id:set() for t in tasks}
    for t in tasks:
        for d in t.dependencies: downstream.setdefault(d,set()).add(t.task_id)
    return tuple(t for t in order if len(downstream.get(t,())) >= max(1, len(tasks)//3))

def workload_ok(employee: Employee) -> bool: return employee.workload <= employee.capacity

def authorize(action: str, level: Authorization, approved: bool = False) -> bool:
    if level == Authorization.PROHIBITED: return False
    if level in {Authorization.HUMAN_APPROVAL_REQUIRED, Authorization.EXECUTIVE_APPROVAL_REQUIRED}: return approved
    return True

def validate_message(message: AgentMessage) -> None:
    if not message.authenticated: raise PermissionError("BLOCK: unauthenticated agent message")
    if not message.authorization_scope: raise PermissionError("BLOCK: missing authorization scope")

def validate_handoff(handoff: Handoff) -> None:
    if handoff.verification_status not in {"VERIFIED", "PARTIAL", "UNKNOWN"}: raise ValueError("invalid verification status")
    if handoff.sender == handoff.receiver: raise ValueError("creator cannot be sole handoff reviewer")

def escalate(task: Task, capability_gap: bool = False, policy_conflict: bool = False, human_approval_required: bool = False) -> bool:
    return task.risk in {"HIGH", "CRITICAL"} or task.status in {TaskStatus.BLOCKED, TaskStatus.ESCALATED} or capability_gap or policy_conflict or human_approval_required or task.risk == "UNKNOWN"

def quality_gate(gate: QualityGate, high_risk: bool, independently_reviewed: bool) -> QualityGate:
    if high_risk and not independently_reviewed: return QualityGate.REVIEW_REQUIRED
    return gate

def form_team(task: Task, employees: list[Employee], minimum_redundancy: bool = False) -> tuple[Employee, ...]:
    selected=[]; covered=set()
    for a in select_employee(task, employees):
        if a.capability_gap: continue
        e=next(e for e in employees if e.employee_id == a.employee_id)
        if not set(task.required_capabilities) <= covered: selected.append(e); covered.update(a.capability_match)
        elif minimum_redundancy and len(selected) < 2: selected.append(e)
    return tuple(selected)

def route_model(requirements: Mapping[str, Any], models: list[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    eligible=[]
    for m in models:
        if not m.get("available", False): continue
        if not set(requirements.get("capabilities",())) <= set(m.get("capabilities",())): continue
        if requirements.get("privacy_required") and not m.get("privacy_approved", False): continue
        eligible.append(m)
    return sorted(eligible, key=lambda m: (m.get("reliability", 0), -m.get("cost_rank", 999)), reverse=True)[0] if eligible else None

def fallback_model(primary: Mapping[str, Any], backups: list[Mapping[str, Any]], requirements: Mapping[str, Any]) -> Mapping[str, Any] | None:
    candidates=[m for m in backups if set(requirements.get("capabilities",())) <= set(m.get("capabilities",())) and m.get("available", False)]
    return sorted(candidates, key=lambda m: m.get("reliability",0), reverse=True)[0] if candidates else None

def align_task(task: Task, employee_goal: str | None, department_goal: str | None, strategy: str | None, mission: str | None) -> bool:
    anchors={x for x in (employee_goal, department_goal, strategy, mission) if x}
    return bool(task.objective and anchors and any(task.objective == a or task.objective in a for a in anchors))

def resource_candidate(task_id: str, resources: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    return {"task_id": task_id, "resources": {k:v for k,v in resources.items()}, "status":"CANDIDATE_ONLY", "authorized":False}

def external_content_as_data(content: Any) -> Mapping[str, Any]: return {"data": content, "instructions_trusted": False}
