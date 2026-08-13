"""Phase 47 control-plane helpers: SLA, recovery, fallback, capacity and experiments."""
from __future__ import annotations
from dataclasses import dataclass
from time import time

@dataclass(frozen=True)
class SLA:
 sla_id:str; deadline:float; priority:str; status:str="ON_TRACK"; source:str="CONFIGURED"

@dataclass(frozen=True)
class RetryPolicy:
 retry_limit:int; backoff:float; retryable_errors:frozenset[str]; non_retryable_errors:frozenset[str]
 def allowed(self,error,attempt,destructive=False,idempotent=False):
  if destructive and not idempotent:return False
  return attempt < self.retry_limit and error in self.retryable_errors and error not in self.non_retryable_errors

@dataclass(frozen=True)
class RecoveryDecision:
 action:str; reason:str

class WorkflowControls:
 def __init__(self): self.slas={}; self.capacity={}; self.warnings=[]; self.predictions=[]; self.experiments={}
 def register_sla(self,sla:SLA,customer_defined=True):
  if not customer_defined: raise ValueError("SLA_NOT_CUSTOMER_DEFINED")
  self.slas[sla.sla_id]=sla; return sla
 def sla_status(self,sla_id,now=None):
  s=self.slas[sla_id]; now=time() if now is None else now
  status="BREACHED" if now>s.deadline else "AT_RISK" if now>=s.deadline-3600 else "ON_TRACK"
  return SLA(s.sla_id,s.deadline,s.priority,status,s.source)
 def recover(self,error,*,retry_allowed,reassign_allowed,escalate=True):
  if retry_allowed:return RecoveryDecision("RETRY","retryable error")
  if reassign_allowed:return RecoveryDecision("REASSIGN","fallback capability available")
  return RecoveryDecision("ESCALATE" if escalate else "FAIL","no safe automatic recovery")
 def fallback(self,primary,alternate,required_capabilities,required_permissions,risk,alternate_capabilities,alternate_permissions):
  if risk=="HIGH" and "HIGH_RISK_EXECUTE" not in alternate_permissions:return RecoveryDecision("ESCALATE","alternate lacks high-risk permission")
  if not set(required_capabilities).issubset(alternate_capabilities):return RecoveryDecision("ESCALATE","capability mismatch")
  if not set(required_permissions).issubset(alternate_permissions):return RecoveryDecision("ESCALATE","permission mismatch")
  return RecoveryDecision("FALLBACK",f"{primary}->{alternate}")
 def set_capacity(self,resource,capacity,active_tasks=0,queue=0,average_latency=0.0,failure_rate=0.0):
  self.capacity[resource]={"capacity":capacity,"active_tasks":active_tasks,"queue":queue,"average_latency":average_latency,"failure_rate":failure_rate}; return self.capacity[resource]
 def rebalance(self,source,target,capability_required):
  s,t=self.capacity[source],self.capacity[target]
  if s["active_tasks"]<=s["capacity"] or t["active_tasks"]>=t["capacity"]:return False
  if capability_required not in t.get("capabilities",{capability_required}):return False
  s["active_tasks"]-=1; t["active_tasks"]+=1; return True
 def warning(self,signal,observed):
  w={"type":"WARNING","signal":signal,"observed":observed,"timestamp":time()}; self.warnings.append(w); return w
 def prediction(self,signal,value,evidence_sufficient):
  p={"type":"PREDICTION","signal":signal,"value":value,"timestamp":time(),"evidence":"MEASURED" if evidence_sufficient else "INSUFFICIENT_DATA"}; self.predictions.append(p); return p
 def experiment(self,experiment_id,hypothesis,metric,population,duration,success_criteria):
  e={"experiment_id":experiment_id,"hypothesis":hypothesis,"metric":metric,"population":population,"duration":duration,"success_criteria":success_criteria,"result":None,"evidence":"NO_DATA"}; self.experiments[experiment_id]=e; return e
 def conclude_experiment(self,experiment_id,result,evidence):
  if evidence not in {"MEASURED","UNKNOWN"}: raise ValueError("EXPERIMENT_EVIDENCE_REQUIRED")
  e=self.experiments[experiment_id]; e["result"]=result; e["evidence"]=evidence; return e
