"""Phase 49 customer productization and production-readiness primitives.

Pure-Python, dependency-free policy/domain layer. External payment and social
integrations remain explicit boundaries and never report success when absent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from time import time
from typing import Any, Mapping
from uuid import uuid4


class AccountStatus(str, Enum):
    PENDING="PENDING"; ACTIVE="ACTIVE"; SUSPENDED="SUSPENDED"; DELETED="DELETED"
class SubscriptionStatus(str, Enum):
    TRIAL="TRIAL"; ACTIVE="ACTIVE"; PAST_DUE="PAST_DUE"; CANCELED="CANCELED"; EXPIRED="EXPIRED"
class BillingState(str, Enum):
    TRIAL="TRIAL"; ACTIVE="ACTIVE"; PAST_DUE="PAST_DUE"; CANCELED="CANCELED"; EXPIRED="EXPIRED"; PAYMENT_NOT_CONNECTED="PAYMENT_NOT_CONNECTED"
class TaskStatus(str, Enum):
    DRAFT="DRAFT"; QUEUED="QUEUED"; RUNNING="RUNNING"; WAITING="WAITING"; REVIEW_REQUIRED="REVIEW_REQUIRED"; COMPLETED="COMPLETED"; FAILED="FAILED"; CANCELED="CANCELED"
class ReadinessLevel(int, Enum):
    NOT_IMPLEMENTED=0; INTERNAL_ONLY=1; TESTABLE=2; BETA=3; PRODUCTION_CANDIDATE=4; PRODUCTION_READY=5

@dataclass(frozen=True)
class Plan:
    plan_id: str; name: str; price: int; currency: str="THB"; billing_period: str="monthly"
    employee_limit: int|None=1; task_limit: int|None=0; knowledge_limit: int|None=0; storage_limit: int|None=0
    tool_access: frozenset[str]=frozenset(); feature_flags: frozenset[str]=frozenset(); status: str="ACTIVE"

PLANS: dict[str, Plan] = {
    "FREE": Plan("FREE","Free",0,employee_limit=1,task_limit=25,knowledge_limit=25,storage_limit=25,tool_access=frozenset({"basic"}),feature_flags=frozenset({"employee","knowledge","task","workflow","result"})),
    "199": Plan("199","Starter",199,employee_limit=2,task_limit=100,knowledge_limit=250,storage_limit=250,tool_access=frozenset({"basic"}),feature_flags=frozenset({"employee","knowledge","memory","task","workflow","result","dashboard","learning","usage"})),
    "399": Plan("399","Team",399,employee_limit=5,task_limit=300,knowledge_limit=750,storage_limit=1000,tool_access=frozenset({"basic","team"}),feature_flags=frozenset({"employee","knowledge","memory","task","workflow","result","dashboard","learning","usage","shared_knowledge","team_workflow"})),
    "699": Plan("699","Department",699,employee_limit=10,task_limit=1000,knowledge_limit=2500,storage_limit=5000,tool_access=frozenset({"basic","team","advanced"}),feature_flags=frozenset({"employee","knowledge","memory","task","workflow","result","dashboard","learning","usage","shared_knowledge","team_workflow","department","advanced_intelligence","team_management"})),
    "1499": Plan("1499","AI Organization",1499,employee_limit=None,task_limit=None,knowledge_limit=None,storage_limit=None,tool_access=frozenset({"basic","team","advanced","custom"}),feature_flags=frozenset({"employee","knowledge","memory","task","workflow","result","dashboard","learning","usage","shared_knowledge","team_workflow","department","advanced_intelligence","team_management","custom_workforce","custom_workflow","organization_governance"})),
}

@dataclass(frozen=True)
class Customer:
    customer_id: str; email: str; status: AccountStatus; created_at: float
@dataclass(frozen=True)
class Tenant:
    tenant_id: str; owner_id: str; business_id: str; plan_id: str; status: str="ACTIVE"; created_at: float=field(default_factory=time)
@dataclass(frozen=True)
class Business:
    business_id: str; tenant_id: str; business_name: str; industry: str; description: str; products: tuple[str,...]; services: tuple[str,...]; target_customers: str; goals: tuple[str,...]; language: str; timezone: str
@dataclass(frozen=True)
class Employee:
    employee_id: str; tenant_id: str; name: str; role: str; objective: str; responsibilities: tuple[str,...]; skills: tuple[str,...]; knowledge_scope: tuple[str,...]; memory_scope: tuple[str,...]; tools: tuple[str,...]; permissions: tuple[str,...]; autonomy_level: str; status: str="ACTIVE"
@dataclass(frozen=True)
class Task:
    task_id: str; tenant_id: str; employee_id: str; title: str; objective: str; status: TaskStatus=TaskStatus.DRAFT; correlation_id: str=field(default_factory=lambda: str(uuid4())); idempotency_key: str|None=None
@dataclass(frozen=True)
class UsageEvent:
    usage_id: str; tenant_id: str; resource: str; quantity: int; timestamp: float

class ProductizationError(Exception): pass
class TenantIsolationError(ProductizationError): pass
class EntitlementError(ProductizationError): pass
class AuthorizationError(ProductizationError): pass
class PaymentNotConnected(ProductizationError): pass

class CustomerProduct:
    """In-memory reference implementation; persistence belongs to existing platform storage."""
    def __init__(self, plans: Mapping[str,Plan]|None=None):
        self.plans=dict(plans or PLANS); self.customers={}; self.tenants={}; self.businesses={}; self.employees={}; self.tasks={}; self.usage=[]; self.audit=[]; self._idem=set()

    def register(self,email:str)->Customer:
        if not email or "@" not in email: raise ValueError("INVALID_EMAIL")
        c=Customer(str(uuid4()),email,AccountStatus.ACTIVE,time()); self.customers[c.customer_id]=c; return c

    def create_tenant(self,customer_id:str,business_id:str,plan_id:str="FREE")->Tenant:
        self._customer(customer_id); self._plan(plan_id); t=Tenant(str(uuid4()),customer_id,business_id,plan_id); self.tenants[t.tenant_id]=t; return t

    def create_business(self,tenant_id:str,**data:Any)->Business:
        self._tenant(tenant_id); required=("business_name","industry","description","products","services","target_customers","goals","language","timezone")
        if any(k not in data for k in required): raise ValueError("BUSINESS_PROFILE_INCOMPLETE")
        b=Business(str(data.get("business_id",uuid4())),tenant_id,data["business_name"],data["industry"],data["description"],tuple(data["products"]),tuple(data["services"]),data["target_customers"],tuple(data["goals"]),data["language"],data["timezone"]); self.businesses[b.business_id]=b; return b

    def entitlement(self,tenant_id:str,feature:str|None=None)->dict[str,Any]:
        t=self._tenant(tenant_id); p=self._plan(t.plan_id); allowed=feature is None or feature in p.feature_flags
        return {"tenant_id":tenant_id,"plan_id":p.plan_id,"feature":feature,"allowed":allowed,"employee_limit":p.employee_limit,"task_limit":p.task_limit,"knowledge_limit":p.knowledge_limit,"tool_access":sorted(p.tool_access)}

    def create_employee(self,tenant_id:str,name:str,role:str,objective:str,**config:Any)->Employee:
        t=self._tenant(tenant_id); p=self._plan(t.plan_id); count=sum(e.tenant_id==tenant_id and e.status=="ACTIVE" for e in self.employees.values())
        if p.employee_limit is not None and count>=p.employee_limit: raise EntitlementError("EMPLOYEE_LIMIT")
        if "employee" not in p.feature_flags: raise EntitlementError("EMPLOYEE_FEATURE_NOT_INCLUDED")
        e=Employee(str(uuid4()),tenant_id,name,role,objective,tuple(config.get("responsibilities",())),tuple(config.get("skills",())),tuple(config.get("knowledge_scope",())),tuple(config.get("memory_scope",())),tuple(config.get("tools",())),tuple(config.get("permissions",())),config.get("autonomy_level","L1_AI_ASSIST")); self.employees[e.employee_id]=e; self._audit(tenant_id,"customer","employee.create",e.employee_id); return e

    def create_task(self,tenant_id:str,employee_id:str,title:str,objective:str,idempotency_key:str|None=None)->Task:
        self._tenant(tenant_id); e=self._employee(employee_id,tenant_id); p=self._plan(self.tenants[tenant_id].plan_id)
        if p.task_limit is not None and self.usage_total(tenant_id,"task")>=p.task_limit: raise EntitlementError("TASK_LIMIT")
        if idempotency_key and idempotency_key in self._idem: raise ProductizationError("IDEMPOTENT_DUPLICATE")
        if idempotency_key: self._idem.add(idempotency_key)
        task=Task(str(uuid4()),tenant_id,e.employee_id,title,objective,TaskStatus.QUEUED,idempotency_key=idempotency_key); self.tasks[task.task_id]=task; self.record_usage(tenant_id,"task"); self._audit(tenant_id,"customer","task.create",task.task_id); return task

    def authorize_tool(self,tenant_id:str,employee_id:str,tool:str,permission:str)->bool:
        e=self._employee(employee_id,tenant_id); p=self._plan(self.tenants[tenant_id].plan_id)
        if "basic" not in p.tool_access and tool not in p.tool_access: raise EntitlementError("TOOL_NOT_ENTITLED")
        if permission not in e.permissions: raise AuthorizationError("PERMISSION_DENIED")
        return True

    def record_usage(self,tenant_id:str,resource:str,quantity:int=1)->UsageEvent:
        self._tenant(tenant_id)
        if quantity<0: raise ValueError("INVALID_USAGE")
        event=UsageEvent(str(uuid4()),tenant_id,resource,quantity,time()); self.usage.append(event); return event
    def usage_total(self,tenant_id:str,resource:str)->int: return sum(x.quantity for x in self.usage if x.tenant_id==tenant_id and x.resource==resource)

    def billing_state(self,tenant_id:str)->BillingState: return BillingState.PAYMENT_NOT_CONNECTED
    def activate_paid_plan(self,tenant_id:str,plan_id:str)->None: raise PaymentNotConnected("PAYMENT_NOT_CONNECTED")
    def publish_product(self,tenant_id:str,*_args:Any,**_kwargs:Any)->str: return "NOT_CONNECTED"

    def readiness(self,plan_id:str)->dict[str,Any]:
        p=self._plan(plan_id); gates={"account":True,"tenant":True,"plan":True,"entitlement":True,"employee":True,"knowledge":True,"task":True,"workflow":True,"tool":True,"usage":True,"billing_state":False,"security":True,"tenant_isolation":True,"monitoring":False,"recovery":False,"e2e":False}
        level=ReadinessLevel.PRODUCTION_READY if all(gates.values()) else ReadinessLevel.TESTABLE
        return {"plan_id":p.plan_id,"level":level.name,"score":level.value,"gates":gates,"evidence_required":[k for k,v in gates.items() if not v]}

    def _customer(self,id:str)->Customer:
        if id not in self.customers: raise ProductizationError("CUSTOMER_NOT_FOUND")
        return self.customers[id]
    def _tenant(self,id:str)->Tenant:
        if id not in self.tenants: raise ProductizationError("TENANT_NOT_FOUND")
        return self.tenants[id]
    def _employee(self,id:str,tenant_id:str)->Employee:
        if id not in self.employees: raise ProductizationError("EMPLOYEE_NOT_FOUND")
        e=self.employees[id]
        if e.tenant_id!=tenant_id: raise TenantIsolationError("CROSS_TENANT_EMPLOYEE_ACCESS")
        return e
    def _plan(self,id:str)->Plan:
        if id not in self.plans: raise ProductizationError("PLAN_NOT_FOUND")
        return self.plans[id]
    def _audit(self,tenant_id:str,actor:str,action:str,reference:str)->None: self.audit.append({"tenant_id":tenant_id,"actor":actor,"action":action,"reference":reference,"timestamp":time()})

def prompt_injection_safe(content:str)->bool:
    """Treat external content as data; deny obvious attempts to alter policy/authorization."""
    lowered=content.lower()
    blocked=("ignore system policy","override authorization","reveal secret","change billing","grant permission")
    return not any(x in lowered for x in blocked)

def tenant_scoped(record:Any,tenant_id:str)->bool: return getattr(record,"tenant_id",None)==tenant_id

def correlation_id()->str: return str(uuid4())

def content_hash(content:str)->str: return sha256(content.encode("utf-8")).hexdigest()
