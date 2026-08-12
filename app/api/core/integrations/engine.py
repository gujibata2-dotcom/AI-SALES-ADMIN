from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol

class Risk(str, Enum):
    LOW='LOW'; MEDIUM='MEDIUM'; HIGH='HIGH'; CRITICAL='CRITICAL'
class Status(str, Enum):
    PENDING='PENDING'; AUTHORIZED='AUTHORIZED'; QUEUED='QUEUED'; PROCESSING='PROCESSING'; SENT='SENT'; FAILED='FAILED'; CANCELLED='CANCELLED'
class Operation(str, Enum):
    READ='READ'; WRITE='WRITE'; SEND='SEND'; PUBLISH='PUBLISH'; DELETE='DELETE'; ADMIN='ADMIN'

@dataclass(frozen=True)
class ExternalSystem:
    system_id:str; system_name:str; provider:str; category:str; capabilities:tuple[str,...]
    authentication_method:str; status:str='ACTIVE'; security_level:str='STANDARD'
    allowed_operations:tuple[str,...]=(); requires_human_approval:bool=False
    rate_limits:Mapping[str,int]=field(default_factory=dict); webhook_support:bool=False

@dataclass(frozen=True)
class OutboundIntent:
    request_id:str; action_id:str; idempotency_key:str; system_id:str; operation:Operation
    content:Mapping[str,Any]; recipient_reference:str|None=None; risk:Risk=Risk.LOW
    authorization_status:str='PENDING'; status:Status=Status.PENDING

@dataclass(frozen=True)
class WebhookEvent:
    event_id:str; provider:str; event_type:str; timestamp:int; signature:str
    payload_reference:str; verification_status:str='UNVERIFIED'

class ExternalProvider(Protocol):
    def register(self)->ExternalSystem: ...
    def connect(self, credential_reference:str)->bool: ...
    def health_check(self)->str: ...
    def authorize(self, operation:Operation)->bool: ...
    def execute(self, intent:OutboundIntent)->Mapping[str,Any]: ...
    def get_status(self, request_id:str)->Status: ...
    def cancel(self, request_id:str)->bool: ...
    def disconnect(self)->None: ...

class MockProvider:
    def __init__(self, system:ExternalSystem): self.system=system
    def register(self): return self.system
    def connect(self, credential_reference): return bool(credential_reference) and credential_reference.startswith('secret-ref:')
    def health_check(self): return 'HEALTHY'
    def authorize(self, operation): return operation.value in self.system.allowed_operations
    def execute(self, intent): return {'mock':True,'request_id':intent.request_id,'status':'SIMULATED','external_side_effect':False}
    def get_status(self, request_id): return Status.SENT
    def cancel(self, request_id): return True
    def disconnect(self): return None

class IntegrationGate:
    def __init__(self, employee_ops:set[str], integration_ops:set[str], approved:bool=True, human_approval:bool=False):
        self.employee_ops=employee_ops; self.integration_ops=integration_ops; self.approved=approved; self.human_approval=human_approval
    def authorize(self, intent:OutboundIntent, system:ExternalSystem, platform_policy:bool=True)->tuple[bool,str]:
        if not self.approved: return False,'GOVERNANCE_BLOCK'
        if intent.operation.value not in self.employee_ops or intent.operation.value not in self.integration_ops: return False,'OPERATION_NOT_ALLOWED'
        if intent.operation.value not in system.allowed_operations: return False,'PLATFORM_OPERATION_UNSUPPORTED'
        if not platform_policy: return False,'PLATFORM_POLICY_BLOCK'
        if intent.risk in (Risk.HIGH,Risk.CRITICAL) and (system.requires_human_approval or not self.human_approval): return False,'HUMAN_APPROVAL_REQUIRED'
        return True,'AUTHORIZED'

class WebhookVerifier:
    def __init__(self, max_age_seconds:int=300): self.max_age_seconds=max_age_seconds
    def verify(self, event:WebhookEvent, now:int, expected_signature:str, seen:set[str])->tuple[bool,str]:
        if event.event_id in seen: return False,'REPLAY_OR_DUPLICATE'
        if event.signature != expected_signature: return False,'INVALID_SIGNATURE'
        if abs(now-event.timestamp)>self.max_age_seconds: return False,'STALE_EVENT'
        seen.add(event.event_id); return True,'VERIFIED'

class Outbox:
    def __init__(self): self.items:dict[str,OutboundIntent]={}
    def put(self, intent):
        if intent.idempotency_key in {x.idempotency_key for x in self.items.values()}: return False
        self.items[intent.request_id]=intent; return True
    def get(self, request_id): return self.items.get(request_id)

class RateLimiter:
    def __init__(self, limits:Mapping[str,int]): self.limits=dict(limits); self.counts={}
    def allow(self, operation:str)->bool:
        n=self.counts.get(operation,0)+1; limit=self.limits.get(operation)
        if limit is not None and n>limit: return False
        self.counts[operation]=n; return True

class BudgetGuard:
    def __init__(self, daily:float|None=None, monthly:float|None=None): self.daily=daily; self.monthly=monthly
    def allow(self, daily_used:float, monthly_used:float, cost:float)->bool:
        return (self.daily is None or daily_used+cost<=self.daily) and (self.monthly is None or monthly_used+cost<=self.monthly)

class DraftMode:
    def prepare(self, intent:OutboundIntent)->dict[str,Any]:
        return {'system_id':intent.system_id,'operation':intent.operation.value,'content':dict(intent.content),'recipient_reference':intent.recipient_reference,'risk':intent.risk.value,'permission':intent.authorization_status,'expected_side_effect':False,'status':'DRAFT'}
