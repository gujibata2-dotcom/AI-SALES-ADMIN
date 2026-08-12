"""Phase 27: bounded agent/tool execution control.

Provider-neutral contracts. No provider is called directly from business logic.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

class Status(str, Enum): ACTIVE="ACTIVE"; DEGRADED="DEGRADED"; UNAVAILABLE="UNAVAILABLE"; DEPRECATED="DEPRECATED"; BLOCKED="BLOCKED"
class Risk(str, Enum): LOW="LOW"; MEDIUM="MEDIUM"; HIGH="HIGH"; CRITICAL="CRITICAL"
class ActionStatus(str, Enum): PLANNED="PLANNED"; AUTHORIZED="AUTHORIZED"; PREPARED="PREPARED"; EXECUTING="EXECUTING"; SUCCEEDED="SUCCEEDED"; FAILED="FAILED"; VERIFICATION_FAILED="VERIFICATION_FAILED"; ROLLED_BACK="ROLLED_BACK"; CANCELLED="CANCELLED"

@dataclass(frozen=True)
class AgentSpec:
    agent_id:str; provider:str; agent_name:str; version:str; capabilities:frozenset[str]; supported_tools:frozenset[str]; supported_tasks:frozenset[str]; security_level:str; status:Status; approval_status:str; cost_profile:dict[str,Any]; reliability_profile:dict[str,Any]

@dataclass(frozen=True)
class ToolSpec:
    tool_id:str; name:str; description:str; category:str; input_schema:dict[str,Any]; output_schema:dict[str,Any]; risk_level:Risk; required_permission:str; reversible:bool; external_side_effect:bool; status:Status

@dataclass(frozen=True)
class AgentTask:
    task_id:str; employee_id:str; agent_id:str; objective:str; constraints:dict[str,Any]; inputs:dict[str,Any]; required_tools:tuple[str,...]; authorization:dict[str,Any]; risk_level:Risk; deadline:str|None; budget:float|None; verification_requirements:dict[str,Any]

@dataclass(frozen=True)
class Action:
    action_id:str; task_id:str; tool_id:str; agent_id:str; operation:str; inputs:dict[str,Any]; expected_output:dict[str,Any]; risk_level:Risk; authorization_status:str=ActionStatus.PLANNED.value; execution_status:str=ActionStatus.PLANNED.value; verification_status:str="PENDING"

class AgentProvider(Protocol):
    def register(self)->dict[str,Any]: ...
    def health_check(self)->dict[str,Any]: ...
    def create_task(self,task:dict[str,Any])->dict[str,Any]: ...
    def execute(self,action:dict[str,Any])->dict[str,Any]: ...
    def cancel(self,task_id:str)->dict[str,Any]: ...
    def get_status(self,task_id:str)->dict[str,Any]: ...
    def get_result(self,task_id:str)->dict[str,Any]: ...

class AuthorizationGate:
    def __init__(self, employee_tools=(), agent_tools=(), permissions=(), human_approved=False):
        self.employee_tools=set(employee_tools); self.agent_tools=set(agent_tools); self.permissions=set(permissions); self.human_approved=human_approved
    def authorize(self,task:AgentTask,tool:ToolSpec)->bool:
        if tool.status in {Status.BLOCKED,Status.UNAVAILABLE,Status.DEPRECATED}: return False
        if self.employee_tools and tool.tool_id not in self.employee_tools: return False
        if self.agent_tools and tool.tool_id not in self.agent_tools: return False
        if tool.required_permission not in self.permissions: return False
        if tool.risk_level in {Risk.HIGH,Risk.CRITICAL} and not self.human_approved: return False
        return True

class ExecutionController:
    def __init__(self,max_steps=20,max_depth=4,max_retries=2,max_agent_calls=10):
        self.max_steps=max_steps; self.max_depth=max_depth; self.max_retries=max_retries; self.max_agent_calls=max_agent_calls
    def preflight(self,task:AgentTask,actions:list[Action])->tuple[bool,str]:
        if not task.employee_id or not task.agent_id: return False,"MISSING_OWNER"
        if len(actions)>self.max_steps: return False,"MAX_STEPS_EXCEEDED"
        if len(actions)>self.max_agent_calls: return False,"MAX_AGENT_CALLS_EXCEEDED"
        if any(a.risk_level in {Risk.HIGH,Risk.CRITICAL} and a.authorization_status!="AUTHORIZED" for a in actions): return False,"HUMAN_APPROVAL_REQUIRED"
        return True,"AUTHORIZED"
    def retryable(self,error_type:str)->bool: return error_type in {"TIMEOUT","PROVIDER_FAILURE","RATE_LIMIT"}

class VerificationGate:
    def verify(self,expected:dict[str,Any],actual:dict[str,Any],schema_valid=True)->dict[str,Any]:
        if not schema_valid: return {"status":"FAILED","reason":"OUTPUT_FAILURE"}
        return {"status":"SUCCESS" if expected.get("result") == actual.get("result") else "UNKNOWN","expected":expected,"actual":actual}

class DryRun:
    def plan(self,actions:list[Action])->list[dict[str,Any]]:
        return [{"action_id":a.action_id,"tool_id":a.tool_id,"inputs":a.inputs,"risk":a.risk_level.value,"external_side_effect":False,"mode":"DRY_RUN"} for a in actions]
