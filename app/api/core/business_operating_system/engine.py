"""Phase 47: business-goal-driven workflow orchestration primitives.

Stdlib-only. This layer owns business goals, processes, workflow state, events,
metrics/outcomes, resource decisions, recovery, governance gates and audit.
External execution remains adapter-driven and authorization-bound.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from time import time
from uuid import uuid4

class GoalStatus(str, Enum): DRAFT="DRAFT"; APPROVED="APPROVED"; ACTIVE="ACTIVE"; AT_RISK="AT_RISK"; ACHIEVED="ACHIEVED"; FAILED="FAILED"; CANCELED="CANCELED"
class WorkflowState(str, Enum): CREATED="CREATED"; QUEUED="QUEUED"; RUNNING="RUNNING"; WAITING="WAITING"; BLOCKED="BLOCKED"; REVIEW_REQUIRED="REVIEW_REQUIRED"; PAUSED="PAUSED"; FAILED="FAILED"; RECOVERING="RECOVERING"; COMPLETED="COMPLETED"; CANCELED="CANCELED"
class Autonomy(str, Enum): L0="L0"; L1="L1"; L2="L2"; L3="L3"; L4="L4"
class Trigger(str, Enum): MANUAL="MANUAL"; SCHEDULED="SCHEDULED"; EVENT="EVENT"; WEBHOOK="WEBHOOK"; THRESHOLD="THRESHOLD"; DEPENDENCY="DEPENDENCY"; HUMAN_APPROVAL="HUMAN_APPROVAL"

TRANSITIONS={
 WorkflowState.CREATED:{WorkflowState.QUEUED,WorkflowState.CANCELED},
 WorkflowState.QUEUED:{WorkflowState.RUNNING,WorkflowState.CANCELED},
 WorkflowState.RUNNING:{WorkflowState.WAITING,WorkflowState.BLOCKED,WorkflowState.REVIEW_REQUIRED,WorkflowState.PAUSED,WorkflowState.FAILED,WorkflowState.COMPLETED,WorkflowState.CANCELED},
 WorkflowState.WAITING:{WorkflowState.RUNNING,WorkflowState.PAUSED,WorkflowState.FAILED,WorkflowState.CANCELED},
 WorkflowState.BLOCKED:{WorkflowState.RUNNING,WorkflowState.RECOVERING,WorkflowState.CANCELED},
 WorkflowState.REVIEW_REQUIRED:{WorkflowState.RUNNING,WorkflowState.CANCELED},
 WorkflowState.PAUSED:{WorkflowState.RUNNING,WorkflowState.CANCELED},
 WorkflowState.FAILED:{WorkflowState.RECOVERING,WorkflowState.CANCELED},
 WorkflowState.RECOVERING:{WorkflowState.RUNNING,WorkflowState.FAILED,WorkflowState.CANCELED},
 WorkflowState.COMPLETED:set(), WorkflowState.CANCELED:set(),
}

@dataclass(frozen=True)
class BusinessGoal:
 goal_id:str; organization_id:str; title:str; description:str; domain:str; priority:int; target:object; metric:str; deadline:float|None; owner:str; status:GoalStatus=GoalStatus.DRAFT; created_at:float=field(default_factory=time); updated_at:float=field(default_factory=time)
@dataclass(frozen=True)
class BusinessProcess:
 process_id:str; name:str; purpose:str; trigger:Trigger; inputs:tuple[str,...]; outputs:tuple[str,...]; steps:tuple[str,...]; dependencies:tuple[str,...]; owners:tuple[str,...]; risk_level:str; version:int=1; status:str="DRAFT"
@dataclass
class Workflow:
 workflow_id:str; organization_id:str; goal_id:str; process_id:str; state:WorkflowState=WorkflowState.CREATED; context:dict=field(default_factory=dict); decisions:list=field(default_factory=list); tasks:list=field(default_factory=list); outputs:list=field(default_factory=list); errors:list=field(default_factory=list); approvals:list=field(default_factory=list); artifacts:list=field(default_factory=list); events:list=field(default_factory=list); outcomes:list=field(default_factory=list); idempotency_keys:set[str]=field(default_factory=set)
@dataclass(frozen=True)
class Metric:
 metric_id:str; goal_id:str; name:str; definition:str; source:str; unit:str; target:object; actual:object|None; timestamp:float; evidence:str="NO_DATA"
@dataclass(frozen=True)
class Outcome:
 outcome_id:str; workflow_id:str; kind:str; status:str; evidence:str; source:str; timestamp:float
@dataclass(frozen=True)
class AuditRecord:
 event_id:str; organization_id:str; actor:str; action:str; result:str; reference:str|None; timestamp:float=field(default_factory=time)

class AuthorizationError(PermissionError): pass
class TransitionError(ValueError): pass
class DataInsufficientError(ValueError): pass

class BusinessOperatingSystem:
 def __init__(self):
  self.goals={}; self.processes={}; self.workflows={}; self.metrics=[]; self.outcomes=[]; self.audit=[]; self.resources={}; self.stops=set(); self.slas={}; self.bottlenecks=[]
 def _audit(self,org,actor,action,result,ref=None): self.audit.append(AuditRecord(str(uuid4()),org,actor,action,result,ref))
 def create_goal(self,organization_id,**kwargs):
  g=BusinessGoal(goal_id=str(uuid4()),organization_id=organization_id,**kwargs); self.goals[g.goal_id]=g; self._audit(organization_id,g.owner,"goal.create","SUCCESS",g.goal_id); return g
 def approve_goal(self,goal_id,actor):
  g=self.goals[goal_id]
  if g.status is not GoalStatus.DRAFT: raise ValueError("GOAL_NOT_DRAFT")
  self.goals[goal_id]=BusinessGoal(**{**g.__dict__,"status":GoalStatus.APPROVED,"updated_at":time()}); self._audit(g.organization_id,actor,"goal.approve","SUCCESS",goal_id); return self.goals[goal_id]
 def create_process(self,**kwargs):
  p=BusinessProcess(process_id=str(uuid4()),**kwargs); self.processes[p.process_id]=p; return p
 def create_workflow(self,organization_id,goal_id,process_id,actor,authorized=False,context=None):
  if not authorized: raise AuthorizationError("WORKFLOW_NOT_AUTHORIZED")
  g=self.goals[goal_id];
  if g.organization_id!=organization_id: raise AuthorizationError("TENANT_MISMATCH")
  w=Workflow(str(uuid4()),organization_id,goal_id,process_id,context=dict(context or {})); self.workflows[w.workflow_id]=w; self._audit(organization_id,actor,"workflow.create","SUCCESS",w.workflow_id); return w
 def transition(self,workflow_id,new_state,actor="system"):
  w=self.workflows[workflow_id]; ns=WorkflowState(new_state)
  if ns not in TRANSITIONS[w.state]: raise TransitionError(f"INVALID_TRANSITION:{w.state.value}->{ns.value}")
  w.state=ns; w.events.append({"type":"STATE_CHANGE","state":ns.value,"timestamp":time()}); self._audit(w.organization_id,actor,"workflow.state",ns.value,workflow_id); return w
 def pause(self,workflow_id,actor): return self.transition(workflow_id,WorkflowState.PAUSED,actor)
 def resume(self,workflow_id,actor): return self.transition(workflow_id,WorkflowState.RUNNING,actor)
 def approve(self,workflow_id,reviewer,decision,reason):
  w=self.workflows[workflow_id]; w.approvals.append({"reviewer":reviewer,"decision":decision,"reason":reason,"timestamp":time()});
  if w.state is WorkflowState.REVIEW_REQUIRED and decision=="APPROVE": self.transition(workflow_id,WorkflowState.RUNNING,reviewer)
  elif decision in {"REJECT","MODIFY"}: self._audit(w.organization_id,reviewer,"workflow.review",decision,workflow_id)
  return w
 def emit_event(self,workflow_id,event,condition=True):
  w=self.workflows[workflow_id]; w.events.append({"type":"EVENT","event":event,"condition":condition,"timestamp":time()}); return condition
 def execute_gate(self,workflow_id,action,actor,authorization,risk="LOW",policy=True,budget=True,idempotency_key=None):
  w=self.workflows[workflow_id]
  if w.organization_id in self.stops or workflow_id in self.stops: raise AuthorizationError("EMERGENCY_STOP")
  if not authorization or not policy or not budget: raise AuthorizationError("ACTION_GATE_DENIED")
  if risk=="HIGH" and not authorization: raise AuthorizationError("HIGH_RISK_DENIED")
  if idempotency_key and idempotency_key in w.idempotency_keys: return False
  if idempotency_key: w.idempotency_keys.add(idempotency_key)
  self._audit(w.organization_id,actor,"action.execute","AUTHORIZED",action); return True
 def emergency_stop(self,scope,actor,reason,organization_id): self.stops.add(scope); self._audit(organization_id,actor,"emergency.stop",reason,scope)
 def record_outcome(self,workflow_id,kind,status,evidence,source):
  if evidence in {"",None}: evidence="NO_DATA"
  o=Outcome(str(uuid4()),workflow_id,kind,status,evidence,source,time()); self.outcomes.append(o); self.workflows[workflow_id].outcomes.append(o.outcome_id); return o
 def record_metric(self,goal_id,name,definition,source,unit,target,actual=None,evidence="NO_DATA"):
  m=Metric(str(uuid4()),goal_id,name,definition,source,unit,target,actual,time(),evidence if actual is not None else "NO_DATA"); self.metrics.append(m); return m
 def roi(self,cost,time_spent,output,business_value):
  if any(v is None for v in (cost,time_spent,output,business_value)) or business_value is None: return {"status":"INSUFFICIENT_DATA"}
  return {"status":"MEASURED","value":(business_value-cost)/cost if cost else None,"cost":cost,"time":time_spent,"output":output,"business_value":business_value}
 def detect_deadlock(self,waits):
  graph={k:set(v) for k,v in waits.items()}; visiting=set(); visited=set()
  def dfs(n):
   if n in visiting:return True
   if n in visited:return False
   visiting.add(n)
   if any(dfs(x) for x in graph.get(n,set())): return True
   visiting.remove(n); visited.add(n); return False
  return any(dfs(n) for n in graph)
 def record_bottleneck(self,kind,reference,observed):
  b={"type":"BOTTLENECK","kind":kind,"reference":reference,"observed":observed,"timestamp":time()}; self.bottlenecks.append(b); return b
 def resource_decision(self,resource,expected_value,risk,cost,time_required,capability=True):
  if not capability:return "REASSIGN"
  if resource.get("quota",1)<=0:return "WAIT"
  if risk=="HIGH":return "USE_STRONGEST_AVAILABLE"
  if expected_value < cost:return "DEFER"
  return "EXECUTE"
 def business_health(self,goal_progress=None,workflow_health=None,employee_health=None,cost=None,risk=None,outcomes=None,feedback=None):
  vals=[v for v in (goal_progress,workflow_health,employee_health,cost,risk,outcomes,feedback) if v is not None]
  return {"status":"NO_DATA" if len(vals)<2 else "MEASURED","signals":vals}
 def autonomous_change_gate(self,major_change, evaluation, risk_assessed, human_approved, versioned, canary):
  if not major_change:return True
  return all((evaluation,risk_assessed,human_approved,versioned,canary))
 def integration_trace(self,phase,reference,evidence_state="NO_DATA"):
  return {"phase":phase,"reference":reference,"evidence_state":evidence_state}
