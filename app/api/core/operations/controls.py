from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class RetryPolicy:
    max_retries:int=3; backoff_seconds:float=1.0; timeout_seconds:int=60
    def validate(self):
        if self.max_retries < 0 or self.max_retries > 10 or self.timeout_seconds <= 0 or self.backoff_seconds < 0: raise ValueError("INVALID_RETRY_POLICY")

@dataclass(frozen=True)
class Scope:
    allowed_actions:frozenset[str]; allowed_targets:frozenset[str]; allowed_data:frozenset[str]; allowed_channels:frozenset[str]
    def permits(self, action:str, target:str, data:set[str], channel:str)->bool:
        return action in self.allowed_actions and target in self.allowed_targets and data <= self.allowed_data and channel in self.allowed_channels

@dataclass(frozen=True)
class Delegation:
    parent_scope:Scope; child_scope:Scope; delegate_permission:bool; depth:int; max_depth:int
    def valid(self)->bool:
        return self.delegate_permission and self.depth <= self.max_depth and self.child_scope.allowed_actions <= self.parent_scope.allowed_actions and self.child_scope.allowed_targets <= self.parent_scope.allowed_targets and self.child_scope.allowed_data <= self.parent_scope.allowed_data and self.child_scope.allowed_channels <= self.parent_scope.allowed_channels

@dataclass(frozen=True)
class Incident:
    level:str; reason:str; execution_id:str

class RecoveryController:
    LEVELS={"INFO","WARNING","HIGH","CRITICAL"}
    def __init__(self, stop_callback:Callable[[],None]): self.stop_callback=stop_callback
    def incident(self, level:str, reason:str, execution_id:str)->Incident:
        if level not in self.LEVELS: raise ValueError("INVALID_INCIDENT_LEVEL")
        if level == "CRITICAL": self.stop_callback()
        return Incident(level,reason,execution_id)

class BudgetController:
    def __init__(self, task:float, workflow:float, team:float, daily:float, monthly:float): self.limits=(task,workflow,team,daily,monthly); self.used=[0.0]*5
    def charge(self, amount:float):
        if amount < 0 or any(self.used[i]+amount > self.limits[i] for i in range(5)): raise PermissionError("BUDGET_EXCEEDED")
        self.used=[x+amount for x in self.used]

class SafeExecutor:
    def __init__(self, retry:RetryPolicy): retry.validate(); self.retry=retry
    def run(self, operation:Callable[[],Any]):
        last=None
        for attempt in range(self.retry.max_retries+1):
            try: return operation(), attempt
            except Exception as exc: last=exc
        raise RuntimeError("RETRY_EXHAUSTED") from last
