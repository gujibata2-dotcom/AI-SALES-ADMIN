from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum
from time import time
from uuid import uuid4
from statistics import mean

class Evidence(str,Enum): FACT="FACT"; INFERENCE="INFERENCE"; PREDICTION="PREDICTION"; RECOMMENDATION="RECOMMENDATION"; SIMULATION="SIMULATION"; NO_DATA="NO_DATA"; UNKNOWN="UNKNOWN"
class BusinessStatus(str,Enum): HEALTHY="HEALTHY"; STABLE="STABLE"; AT_RISK="AT_RISK"; CRITICAL="CRITICAL"; UNKNOWN="UNKNOWN"
class AnomalyStatus(str,Enum): KNOWN="KNOWN_ANOMALY"; POSSIBLE="POSSIBLE_ANOMALY"; CONFIRMED="CONFIRMED_ANOMALY"
class DecisionStatus(str,Enum): DRAFT="DRAFT"; ANALYZING="ANALYZING"; REVIEW_REQUIRED="REVIEW_REQUIRED"; APPROVED="APPROVED"; REJECTED="REJECTED"; EXECUTED="EXECUTED"; VERIFIED="VERIFIED"; FAILED="FAILED"

@dataclass(frozen=True)
class BusinessState:
 business_state_id:str; organization_id:str; timestamp:float; goals:object; metrics:object; workflows:object; workforce:object; customers:object; operations:object; risks:object; opportunities:object; financial_state:object; knowledge_state:object; status:BusinessStatus
@dataclass(frozen=True)
class Signal:
 signal_id:str; kind:str; source:str; timestamp:float; confidence:float; evidence:Evidence; status:str="OBSERVED"; details:dict=field(default_factory=dict)
@dataclass(frozen=True)
class DecisionOption:
 option_id:str; name:str; expected_value:object; cost:object; risk:object; time:object; resources:object; dependencies:object; opportunity_cost:object; second_order_effects:object; reversibility:str
@dataclass
class Decision:
 decision_id:str; goal:str; context:object; problem:str; options:list; constraints:object; evidence:list; risks:list; tradeoffs:list; recommendation:object=None; confidence:str="VERY_LOW"; approval_required:bool=True; decision:object=None; outcome:object=None; status:DecisionStatus=DecisionStatus.DRAFT; assumptions:list=field(default_factory=list); audit:list=field(default_factory=list)
@dataclass(frozen=True)
class Assumption:
 assumption_id:str; statement:str; importance:str; evidence:object; confidence:float; validation_status:str="UNVALIDATED"
@dataclass(frozen=True)
class Scenario:
 scenario_id:str; kind:str; assumptions:object; inputs:object; expected_outcomes:object; risks:object; uncertainty:object; label:str="SIMULATION"
@dataclass(frozen=True)
class Forecast:
 forecast_id:str; metric:str; value:object; confidence_interval:object; time_horizon:str; assumptions:object; evidence:Evidence
@dataclass(frozen=True)
class Risk:
 risk_id:str; description:str; probability:object; impact:object; severity:str; evidence:object; mitigation:object; owner:object; status:str
@dataclass(frozen=True)
class Opportunity:
 opportunity_id:str; kind:str; description:str; evidence:object; expected_value:object; cost:object; risk:object; confidence:float
@dataclass(frozen=True)
class ExecutiveAlert:
 alert_id:str; level:str; why_it_matters:str; evidence:object; impact:object; recommended_action:str; timestamp:float

class DecisionAuthorizationError(PermissionError): pass
class InsufficientEvidence(ValueError): pass

class BusinessIntelligence:
 def __init__(self): self.states={}; self.signals=[]; self.decisions={}; self.journal=[]; self.alerts=[]; self.overrides=[]; self.knowledge=[]
 def state(self,organization_id,**parts):
  vals=[parts.get(k) for k in ("goals","metrics","workflows","workforce","customers","operations","risks","opportunities","financial_state","knowledge_state")]
  status=BusinessStatus.UNKNOWN if not any(v is not None for v in vals) else BusinessStatus.STABLE
  s=BusinessState(str(uuid4()),organization_id,time(),*vals,status); self.states[s.business_state_id]=s; return s
 def signal(self,kind,source,confidence,evidence=Evidence.FACT,details=None,status="OBSERVED"):
  if not 0<=confidence<=1: raise ValueError("CONFIDENCE_RANGE")
  s=Signal(str(uuid4()),kind,source,time(),confidence,Evidence(evidence),status,details or {}); self.signals.append(s); return s
 def anomaly(self,kind,data_points,baseline=None):
  if len(data_points)<3:return self.signal("anomaly",kind,0.0,Evidence.UNKNOWN,{"status":AnomalyStatus.POSSIBLE.value,"reason":"INSUFFICIENT_DATA"},AnomalyStatus.POSSIBLE.value)
  if baseline is None:return self.signal("anomaly",kind,0.2,Evidence.UNKNOWN,{"status":AnomalyStatus.POSSIBLE.value},AnomalyStatus.POSSIBLE.value)
  deviation=abs(data_points[-1]-baseline)/(abs(baseline) or 1); status=AnomalyStatus.CONFIRMED if deviation>=.2 else AnomalyStatus.KNOWN
  return self.signal("anomaly",kind,min(1,deviation),Evidence.FACT,{"deviation":deviation,"status":status.value},status.value)
 def trend(self,values,time_window):
  if len(values)<3:return {"trend":"unknown","time_window":time_window,"data_points":len(values),"confidence":0,"evidence":"UNKNOWN"}
  delta=values[-1]-values[0]; avg=mean(values); direction="stable" if abs(delta)<=abs(avg)*.02 else ("upward" if delta>0 else "downward")
  return {"trend":direction,"time_window":time_window,"data_points":len(values),"confidence":min(1,len(values)/10),"evidence":"FACT"}
 def drivers(self,metric,drivers,evidence): return [{"metric":metric,"driver":d,"evidence":e,"classification":"OBSERVED" if e else "HYPOTHESIS"} for d,e in zip(drivers,evidence)]
 def root_cause(self,problem,candidates,evidence,validated=False): return {"problem":problem,"candidates":[{"cause":c,"evidence":e,"status":"ROOT_CAUSE" if validated else "CANDIDATE"} for c,e in zip(candidates,evidence)]}
 def create_decision(self,goal,context,problem,options,constraints=()):
  if not options: raise ValueError("DECISION_OPTIONS_REQUIRED")
  d=Decision(str(uuid4()),goal,context,problem,list(options),constraints,[],[],[]); self.decisions[d.decision_id]=d; return d
 def compare(self,decision_id):
  d=self.decisions[decision_id]; rows=[]
  for o in d.options: rows.append({"option":o.name,"expected_value":o.expected_value,"cost":o.cost,"risk":o.risk,"time":o.time,"resources":o.resources,"opportunity_cost":o.opportunity_cost,"second_order_effects":o.second_order_effects,"reversibility":o.reversibility})
  return rows
 def recommend(self,decision_id,evidence,confidence="LOW"):
  d=self.decisions[decision_id]; d.evidence=list(evidence); d.confidence=confidence; d.recommendation=max(d.options,key=lambda o:(o.expected_value if isinstance(o.expected_value,(int,float)) else 0)-(o.cost if isinstance(o.cost,(int,float)) else 0)); d.status=DecisionStatus.REVIEW_REQUIRED; return d.recommendation
 def sensitivity(self,assumptions,changed): return "ROBUST" if not changed else ("HIGHLY_SENSITIVE" if len(changed)>len(assumptions)/2 else "SENSITIVE")
 def scenario(self,kind,assumptions,inputs,expected_outcomes,risks,uncertainty): return Scenario(str(uuid4()),kind,assumptions,inputs,expected_outcomes,risks,uncertainty)
 def what_if(self,question,result=None): return {"question":question,"result":result,"type":"SIMULATION","evidence":"SIMULATION"}
 def counterfactual(self,question,result=None): return {"question":question,"result":result,"type":"SIMULATION","evidence":"SIMULATION"}
 def forecast(self,metric,values,time_horizon,assumptions,quality_threshold=.6):
  if len(values)<5:return Forecast(str(uuid4()),metric,None,None,time_horizon,assumptions,Evidence.UNKNOWN)
  if quality_threshold>len(values)/10:return Forecast(str(uuid4()),metric,None,None,time_horizon,assumptions,Evidence.UNKNOWN)
  return Forecast(str(uuid4()),metric,values[-1],None,time_horizon,assumptions,Evidence.PREDICTION)
 def risk(self,description,probability,impact,severity,evidence,mitigation,owner,status="OPEN"): return Risk(str(uuid4()),description,probability,impact,severity,evidence,mitigation,owner,status)
 def opportunity(self,kind,description,evidence,expected_value,cost,risk,confidence): return Opportunity(str(uuid4()),kind,description,evidence,expected_value,cost,risk,confidence)
 def prioritize(self,items): return sorted(items,key=lambda x:sum((getattr(x,k,0) if isinstance(getattr(x,k,0),(int,float)) else 0) for k in ("expected_value","confidence")),reverse=True)
 def alert(self,level,why,evidence,impact,action):
  a=ExecutiveAlert(str(uuid4()),level,why,evidence,impact,action,time()); self.alerts.append(a); return a
 def approve(self,decision_id,actor,risk_level="HIGH",authorized=False,comment=""):
  d=self.decisions[decision_id]
  if risk_level in {"HIGH","CRITICAL"} and not authorized: raise DecisionAuthorizationError("HUMAN_APPROVAL_REQUIRED")
  d.status=DecisionStatus.APPROVED; d.audit.append({"actor":actor,"action":"approve","timestamp":time(),"comment":comment}); return d
 def execute_via_phase47(self,decision_id,workflow_engine,workflow_id,actor,authorized=False):
  d=self.decisions[decision_id]
  if d.status is not DecisionStatus.APPROVED: raise DecisionAuthorizationError("DECISION_NOT_APPROVED")
  if not authorized: raise DecisionAuthorizationError("EXECUTION_NOT_AUTHORIZED")
  result=workflow_engine.execute_gate(workflow_id,"decision.execute",actor,True,idempotency_key=decision_id); d.status=DecisionStatus.EXECUTED; return result
 def override(self,decision_id,actor,reason,new_decision):
  d=self.decisions[decision_id]; record={"decision_id":decision_id,"actor":actor,"reason":reason,"timestamp":time(),"previous_decision":d.decision,"new_decision":new_decision}; self.overrides.append(record); d.decision=new_decision; return record
 def journal_entry(self,decision_id,context,reason,alternatives,assumptions,evidence,approval,execution,outcome,lesson):
  j={"decision_id":decision_id,"context":context,"reason":reason,"alternatives":alternatives,"assumptions":assumptions,"evidence":evidence,"approval":approval,"execution":execution,"outcome":outcome,"lesson":lesson}; self.journal.append(j); return j
 def effectiveness(self,expected,actual):
  if expected is None or actual is None:return {"status":"NO_DATA"}
  if not isinstance(expected,(int,float)) or not isinstance(actual,(int,float)):return {"status":"UNKNOWN"}
  return {"status":"MEASURED","expected":expected,"actual":actual,"error":actual-expected,"absolute_error":abs(actual-expected)}
 def disagreement(self,analyses):
  return {"analyses":analyses,"basis":["evidence","assumptions","uncertainty"],"majority_vote":False}
 def brief(self,period,**sections): return {"period":period,"what_changed":sections.get("what_changed",[]),"what_matters":sections.get("what_matters",[]),"at_risk":sections.get("at_risk",[]),"opportunities":sections.get("opportunities",[]),"decisions_needed":sections.get("decisions_needed",[]),"next":sections.get("next",[])}
 def knowledge_trace(self,reference,freshness,provenance,confidence,scope): return {"reference":reference,"freshness":freshness,"provenance":provenance,"confidence":confidence,"scope":scope}
