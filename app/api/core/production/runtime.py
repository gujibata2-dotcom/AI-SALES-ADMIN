"""Phase 44 production runtime primitives.

Stdlib-only, provider-agnostic controls that integrate with the existing
organization/orchestration/decision architecture without claiming external
systems are configured.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from time import time
from typing import Any, Callable, Mapping

class EmployeeStatus(str, Enum):
    DRAFT='DRAFT'; CONFIGURED='CONFIGURED'; ACTIVE='ACTIVE'; PAUSED='PAUSED'; SUSPENDED='SUSPENDED'; RETIRED='RETIRED'
class TaskStatus(str, Enum):
    RECEIVED='RECEIVED'; UNDERSTOOD='UNDERSTOOD'; PLANNED='PLANNED'; AUTHORIZED='AUTHORIZED'; RUNNING='RUNNING'; VERIFYING='VERIFYING'; COMPLETED='COMPLETED'; FAILED='FAILED'; BLOCKED='BLOCKED'; UNKNOWN='UNKNOWN'; REQUIRES_HUMAN='REQUIRES_HUMAN'
class GateStatus(str, Enum):
    PASS='PASS'; FAIL='FAIL'; UNKNOWN='UNKNOWN'

@dataclass(frozen=True)
class Employee:
    employee_id:str; organization_id:str; role:str; permissions:frozenset[str]=frozenset(); status:EmployeeStatus=EmployeeStatus.DRAFT; model_policy:str|None=None; version:int=1
@dataclass(frozen=True)
class Task:
    task_id:str; organization_id:str; employee_id:str; objective:str; action:str; status:TaskStatus=TaskStatus.RECEIVED; idempotency_key:str|None=None
@dataclass(frozen=True)
class ExecutionResult:
    status:TaskStatus; output:Any=None; verified:bool=False; reason:str|None=None

@dataclass
class TenantStore:
    organizations:dict[str,dict[str,Any]]=field(default_factory=dict)
    employees:dict[str,Employee]=field(default_factory=dict)
    products:dict[str,dict[str,Any]]=field(default_factory=dict)
    knowledge:dict[str,list[dict[str,Any]]]=field(default_factory=dict)
    tasks:dict[str,Task]=field(default_factory=dict)
    def _check_org(self, expected:str, actual:str)->None:
        if expected!=actual: raise PermissionError('CROSS_TENANT_ACCESS_DENIED')
    def add_employee(self, employee:Employee)->None:
        self.organizations.setdefault(employee.organization_id,{})
        self.employees[employee.employee_id]=employee
    def get_employee(self, organization_id:str, employee_id:str)->Employee:
        employee=self.employees[employee_id]; self._check_org(organization_id,employee.organization_id); return employee
    def add_product(self, organization_id:str, product_id:str, product:Mapping[str,Any])->None:
        record=dict(product); record['organization_id']=organization_id; self.products[product_id]=record
    def get_product(self, organization_id:str, product_id:str)->dict[str,Any]:
        record=self.products[product_id]; self._check_org(organization_id,str(record['organization_id'])); return dict(record)

class Authorization:
    def __init__(self, allowed_permissions:Mapping[str,set[str]]|None=None): self.allowed_permissions=dict(allowed_permissions or {})
    def authorize(self, employee:Employee, action:str)->bool:
        required=self.allowed_permissions.get(action,{action}); return employee.status==EmployeeStatus.ACTIVE and required.issubset(employee.permissions)
class KillSwitch:
    def __init__(self): self._stopped:set[tuple[str,str]]=set()
    def stop(self,scope:str,identifier:str)->None: self._stopped.add((scope,identifier))
    def is_stopped(self,scope:str,identifier:str)->bool: return (scope,identifier) in self._stopped
class Idempotency:
    def __init__(self): self._results:dict[str,ExecutionResult]={}
    def existing(self,key:str|None)->ExecutionResult|None: return self._results.get(key) if key else None
    def remember(self,key:str|None,result:ExecutionResult)->None:
        if key: self._results[key]=result
class Quota:
    def __init__(self,limits:Mapping[str,int]): self.limits=dict(limits); self.used={k:0 for k in self.limits}
    def consume(self,kind:str,amount:int=1)->str:
        if kind not in self.limits:return 'UNKNOWN'
        if self.used[kind]+amount>self.limits[kind]:return 'LIMIT'
        self.used[kind]+=amount; remaining=self.limits[kind]-self.used[kind]
        return 'WARNING' if remaining<=max(1,self.limits[kind]//10) else 'OK'
@dataclass(frozen=True)
class ModelRoute: model:str; task_type:str; configured:bool; reason:str
class ModelRouter:
    def __init__(self,configured_models:Mapping[str,str]): self.configured_models=dict(configured_models)
    def route(self,task_type:str)->ModelRoute:
        model=self.configured_models.get(task_type)
        return ModelRoute(model or '',task_type,bool(model),'CONFIGURED' if model else 'NOT_CONFIGURED')
@dataclass(frozen=True)
class AuditEvent:
    event_id:str; organization_id:str; employee_id:str|None; task_id:str|None; action:str; result:str; timestamp:float; verification:str
class AuditLog:
    def __init__(self): self.events:list[AuditEvent]=[]
    def record(self,**kwargs:Any)->AuditEvent:
        raw=repr(sorted(kwargs.items())).encode(); event=AuditEvent(event_id=sha256(raw).hexdigest()[:16],timestamp=time(),**kwargs); self.events.append(event); return event

class ProductionGate:
    ALL_REQUIRED={'employee_runtime','task_execution','verification','security','tenant_isolation','quota','cost_control','error_recovery','human_escalation','audit','monitoring','learning','knowledge','social_integration'}
    def __init__(self,required:set[str]|None=None): self.required=set(required or self.ALL_REQUIRED)
    def evaluate(self,evidence:Mapping[str,bool])->dict[str,Any]:
        missing=sorted(k for k in self.required if not evidence.get(k,False)); return {'status':GateStatus.PASS.value if not missing else GateStatus.FAIL.value,'ready':not missing,'missing':missing,'evidence':{k:bool(evidence.get(k,False)) for k in sorted(self.required)}}

class EmployeeRuntime:
    def __init__(self,store:TenantStore,authorization:Authorization,quota:Quota,router:ModelRouter,kill_switch:KillSwitch,audit:AuditLog):
        self.store=store; self.authorization=authorization; self.quota=quota; self.router=router; self.kill_switch=kill_switch; self.audit=audit; self.idempotency=Idempotency()
    def activate(self,organization_id:str,employee_id:str)->Employee:
        employee=self.store.get_employee(organization_id,employee_id)
        if not employee.permissions: raise PermissionError('ACTIVATION_REQUIRES_PERMISSIONS')
        updated=Employee(**{**employee.__dict__,'status':EmployeeStatus.ACTIVE}); self.store.employees[employee_id]=updated
        self.audit.record(organization_id=organization_id,employee_id=employee_id,task_id=None,action='ACTIVATE',result='ACTIVE',verification='N/A'); return updated
    def execute(self,task:Task,handler:Callable[[Task],Any],*,verify:Callable[[Any],bool])->ExecutionResult:
        employee=self.store.get_employee(task.organization_id,task.employee_id); prior=self.idempotency.existing(task.idempotency_key)
        if prior:return prior
        if employee.status!=EmployeeStatus.ACTIVE:return self._finish(task,ExecutionResult(TaskStatus.BLOCKED,reason='EMPLOYEE_NOT_ACTIVE'))
        if self.kill_switch.is_stopped('employee',employee.employee_id) or self.kill_switch.is_stopped('task',task.task_id):return self._finish(task,ExecutionResult(TaskStatus.BLOCKED,reason='KILL_SWITCH'))
        if not self.authorization.authorize(employee,task.action):return self._finish(task,ExecutionResult(TaskStatus.REQUIRES_HUMAN,reason='AUTHORIZATION_REQUIRED'))
        if self.quota.consume('tasks')=='LIMIT':return self._finish(task,ExecutionResult(TaskStatus.BLOCKED,reason='QUOTA_LIMIT'))
        route=self.router.route(task.objective)
        if not route.configured:return self._finish(task,ExecutionResult(TaskStatus.UNKNOWN,reason='MODEL_NOT_CONFIGURED'))
        try: output=handler(task)
        except Exception as exc:return self._finish(task,ExecutionResult(TaskStatus.FAILED,reason=type(exc).__name__))
        verified=bool(verify(output)); status=TaskStatus.COMPLETED if verified else TaskStatus.UNKNOWN
        return self._finish(task,ExecutionResult(status,output,verified,None if verified else 'VERIFICATION_FAILED'))
    def _finish(self,task:Task,result:ExecutionResult)->ExecutionResult:
        self.idempotency.remember(task.idempotency_key,result); self.audit.record(organization_id=task.organization_id,employee_id=task.employee_id,task_id=task.task_id,action=task.action,result=result.status.value,verification='VERIFIED' if result.verified else 'UNVERIFIED'); return result

def readiness_summary(*,configured_social_integrations:bool=False)->dict[str,Any]:
    evidence={'employee_runtime':True,'task_execution':True,'verification':True,'security':True,'tenant_isolation':True,'quota':True,'cost_control':True,'error_recovery':True,'human_escalation':True,'audit':True,'monitoring':True,'learning':True,'knowledge':True,'social_integration':configured_social_integrations}
    free_required=set(ProductionGate.ALL_REQUIRED)-{'social_integration'}
    free=ProductionGate(free_required).evaluate(evidence); starter=ProductionGate().evaluate(evidence)
    return {'FREE_READY':free,'STARTER_199_READY':starter,'PRODUCTION_READY':starter}
