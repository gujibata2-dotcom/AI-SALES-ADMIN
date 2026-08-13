from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from statistics import mean
from time import time
from uuid import uuid4

class Evidence(str, Enum):
    FACT='FACT'; INFERENCE='INFERENCE'; PREDICTION='PREDICTION'; RECOMMENDATION='RECOMMENDATION'; SIMULATION='SIMULATION'; NO_DATA='NO_DATA'; UNKNOWN='UNKNOWN'
class BusinessStatus(str, Enum): HEALTHY='HEALTHY'; STABLE='STABLE'; AT_RISK='AT_RISK'; CRITICAL='CRITICAL'; UNKNOWN='UNKNOWN'
class AnomalyStatus(str, Enum): POSSIBLE='POSSIBLE'; CONFIRMED='CONFIRMED'; FALSE_POSITIVE='FALSE_POSITIVE'; UNKNOWN='UNKNOWN'
class DecisionStatus(str, Enum): DRAFT='DRAFT'; ANALYZING='ANALYZING'; REVIEW_REQUIRED='REVIEW_REQUIRED'; APPROVED='APPROVED'; REJECTED='REJECTED'; EXECUTED='EXECUTED'; VERIFIED='VERIFIED'; FAILED='FAILED'
class Confidence(str, Enum): VERY_LOW='VERY_LOW'; LOW='LOW'; MEDIUM='MEDIUM'; HIGH='HIGH'; VERY_HIGH='VERY_HIGH'
class AssumptionStatus(str, Enum): VALIDATED='VALIDATED'; UNVALIDATED='UNVALIDATED'; CONTESTED='CONTESTED'; INVALIDATED='INVALIDATED'

@dataclass(frozen=True)
class BusinessEvent:
    business_event_id:str; tenant_id:str; event_type:str; source:str; timestamp:float; entity:object; payload:object; confidence:float; provenance:object
@dataclass(frozen=True)
class Metric:
    metric_id:str; name:str; value:object; unit:str; period:str; source:str; timestamp:float; definition:str; confidence:float; evidence:Evidence
@dataclass(frozen=True)
class BusinessState:
    business_state_id:str; organization_id:str; timestamp:float; goals:object; metrics:object; customers:object; operations:object; workforce:object; workflows:object; risks:object; opportunities:object; financial_state:object; knowledge_state:object; status:BusinessStatus
@dataclass(frozen=True)
class Signal:
    signal_id:str; kind:str; source:str; timestamp:float; evidence:object; confidence:float; details:object
@dataclass(frozen=True)
class DecisionOption:
    option_id:str; name:str; expected_value:object; cost:object; risk:object; time:object; resources:object; dependencies:object; opportunity_cost:object; second_order_effects:object; reversibility:str
@dataclass
class Decision:
    decision_id:str; goal:str; problem:str; context:object; constraints:object; evidence:list; options:list; assumptions:list; risks:list; tradeoffs:list; recommendation:object=None; confidence:Confidence=Confidence.VERY_LOW; approval_required:bool=True; decision:object=None; outcome:object=None; status:DecisionStatus=DecisionStatus.DRAFT; audit:list=field(default_factory=list)
@dataclass(frozen=True)
class Assumption:
    assumption_id:str; statement:str; importance:str; evidence:object; confidence:float; status:AssumptionStatus=AssumptionStatus.UNVALIDATED
@dataclass(frozen=True)
class Scenario:
    scenario_id:str; kind:str; assumptions:object; inputs:object; constraints:object; expected_outcomes:object; risks:object; uncertainty:object; label:str='SIMULATION'
@dataclass(frozen=True)
class Forecast:
    forecast_id:str; metric:str; forecast:object; time_horizon:str; assumptions:object; confidence:object; uncertainty:object; status:str
@dataclass(frozen=True)
class Risk:
    risk_id:str; description:str; probability:object; impact:object; severity:str; evidence:object; mitigation:object; owner:object; status:str
@dataclass(frozen=True)
class Opportunity:
    opportunity_id:str; kind:str; description:str; evidence:object; expected_value:object; cost:object; risk:object; confidence:object
@dataclass(frozen=True)
class ExecutiveAlert:
    alert_id:str; level:str; why_it_matters:str; evidence:object; impact:object; recommended_action:str; timestamp:float

class DecisionAuthorizationError(PermissionError): pass
class InsufficientEvidence(ValueError): pass

class BusinessIntelligence:
    def __init__(self):
        self.events=[]; self.metrics=[]; self.states={}; self.signals=[]; self.decisions={}; self.alerts=[]; self.journal=[]; self.overrides=[]
    @staticmethod
    def _id(prefix): return f'{prefix}_{uuid4().hex}'
    @staticmethod
    def _confidence(value):
        if not 0 <= value <= 1: raise ValueError('CONFIDENCE_RANGE')
        return value
    def event(self,tenant_id,event_type,source,entity,payload,confidence,provenance):
        e=BusinessEvent(self._id('evt'),tenant_id,event_type,source,time(),entity,payload,self._confidence(confidence),provenance); self.events.append(e); return e
    def metric(self,name,value,unit,period,source,definition,confidence,evidence=Evidence.FACT):
        if value is None or not source or not definition: raise InsufficientEvidence('METRIC_EVIDENCE_REQUIRED')
        m=Metric(self._id('metric'),name,value,unit,period,source,time(),definition,self._confidence(confidence),Evidence(evidence)); self.metrics.append(m); return m
    def state(self,organization_id,**parts):
        keys=('goals','metrics','customers','operations','workforce','workflows','risks','opportunities','financial_state','knowledge_state')
        vals=[parts.get(k) for k in keys]; present=sum(v is not None for v in vals)
        status=BusinessStatus.UNKNOWN if present < 2 else BusinessStatus.STABLE
        s=BusinessState(self._id('state'),organization_id,time(),*vals,status); self.states[s.business_state_id]=s; return s
    def signal(self,kind,source,evidence,confidence,details=None):
        s=Signal(self._id('sig'),kind,source,time(),evidence,self._confidence(confidence),details or {}); self.signals.append(s); return s
    def anomaly(self,kind,data,baseline=None):
        if len(data)<3 or baseline is None: return self.signal('ANOMALY',kind,Evidence.UNKNOWN,0,{'status':AnomalyStatus.UNKNOWN.value,'reason':'INSUFFICIENT_DATA'})
        deviation=abs(data[-1]-baseline)/(abs(baseline) or 1)
        status=AnomalyStatus.CONFIRMED if deviation >= .2 else AnomalyStatus.POSSIBLE
        return self.signal('ANOMALY',kind,Evidence.FACT,min(1,deviation),{'status':status.value,'deviation':deviation})
    def trend(self,values,time_window):
        if len(values)<3:return {'direction':'UNKNOWN','time_window':time_window,'data_points':len(values),'confidence':0,'evidence':Evidence.UNKNOWN.value}
        avg=mean(values); delta=values[-1]-values[0]
        direction='STABLE' if abs(delta)<=max(abs(avg)*.02,1e-12) else ('UPWARD' if delta>0 else 'DOWNWARD')
        return {'direction':direction,'time_window':time_window,'data_points':len(values),'confidence':min(1,len(values)/10),'evidence':Evidence.FACT.value}
    def drivers(self,metric,items):
        return [{'driver':name,'classification':classification,'evidence':evidence,'confidence':confidence} for name,classification,evidence,confidence in items]
    def root_cause(self,problem,candidates,validated=False):
        return {'problem':problem,'candidates':candidates,'status':'ROOT_CAUSE' if validated else 'CANDIDATE','unknowns':[] if validated else ['validation_required']}
    def decision(self,goal,problem,context,options,constraints=(),risks=(),tradeoffs=()):
        if not options: raise ValueError('DECISION_OPTIONS_REQUIRED')
        d=Decision(self._id('decision'),goal,problem,context,constraints,[],list(options),[],list(risks),list(tradeoffs)); self.decisions[d.decision_id]=d; return d
    def compare_options(self,decision_id):
        d=self.decisions[decision_id]
        return [o.__dict__.copy() if hasattr(o,'__dict__') else o for o in d.options]
    def recommend(self,decision_id,evidence,confidence=Confidence.LOW):
        d=self.decisions[decision_id]
        if not evidence: raise InsufficientEvidence('RECOMMENDATION_EVIDENCE_REQUIRED')
        d.evidence=list(evidence); d.recommendation=d.options[0]; d.confidence=Confidence(confidence); d.status=DecisionStatus.REVIEW_REQUIRED; return d
    def sensitivity(self,assumptions,changed):
        if not assumptions:return 'UNKNOWN'
        ratio=len(changed)/len(assumptions); return 'ROBUST' if ratio==0 else ('HIGHLY_SENSITIVE' if ratio>.5 else 'SENSITIVE')
    def scenario(self,kind,assumptions,inputs,constraints,expected_outcomes,risks,uncertainty):
        return Scenario(self._id('scenario'),kind,assumptions,inputs,constraints,expected_outcomes,risks,uncertainty)
    def simulation(self,variables,constraints,assumptions,scenarios,outcomes=None):
        return {'type':Evidence.SIMULATION.value,'variables':variables,'constraints':constraints,'assumptions':assumptions,'scenarios':scenarios,'outcomes':outcomes}
    def what_if(self,question,result=None,label='SIMULATION'): return {'question':question,'result':result,'label':label,'evidence':label}
    def counterfactual(self,question,result=None): return self.what_if(question,result,'SIMULATION')
    def forecast(self,metric,values,time_horizon,assumptions,data_quality):
        if len(values)<5 or data_quality < .6:return Forecast(self._id('forecast'),metric,None,time_horizon,assumptions,None,None,'FORECAST_UNAVAILABLE')
        return Forecast(self._id('forecast'),metric,values[-1],time_horizon,assumptions,data_quality,{'method':'baseline','uncertainty':'UNKNOWN'},'PREDICTION')
    def risk(self,description,probability,impact,severity,evidence,mitigation,owner,status='OPEN'): return Risk(self._id('risk'),description,probability,impact,severity,evidence,mitigation,owner,status)
    def opportunity(self,kind,description,evidence,expected_value,cost,risk,confidence): return Opportunity(self._id('opp'),kind,description,evidence,expected_value,cost,risk,confidence)
    def early_warning(self,signal,why,evidence,impact,action): return self.alert('WARNING',why,evidence,impact,action)
    def alert(self,level,why,evidence,impact,action):
        a=ExecutiveAlert(self._id('alert'),level,why,evidence,impact,action,time()); self.alerts.append(a); return a
    def prioritize(self,items):
        def score(x):
            vals=[]
            for k in ('impact','urgency','risk','value','expected_value','confidence'):
                v=x.get(k,0) if isinstance(x,dict) else getattr(x,k,0)
                vals.append(v if isinstance(v,(int,float)) else 0)
            return sum(vals)
        return sorted(items,key=score,reverse=True)
    def brief(self,period,**sections):
        return {'period':period,'what_changed':sections.get('what_changed',[]),'what_matters':sections.get('what_matters',[]),'at_risk':sections.get('at_risk',[]),'opportunities':sections.get('opportunities',[]),'decisions_required':sections.get('decisions_required',[]),'next':sections.get('next',[])}
    def approve(self,decision_id,actor,risk_level,authorized=False,comment=''):
        d=self.decisions[decision_id]
        if risk_level in ('HIGH','CRITICAL') and not authorized: raise DecisionAuthorizationError('HUMAN_APPROVAL_REQUIRED')
        d.status=DecisionStatus.APPROVED; d.audit.append({'actor':actor,'reason':comment,'timestamp':time(),'action':'APPROVE'}); return d
    def execute_via_phase47(self,decision_id,workflow_engine,workflow_id,actor,authorized=False):
        d=self.decisions[decision_id]
        if d.status is not DecisionStatus.APPROVED or not authorized: raise DecisionAuthorizationError('EXECUTION_NOT_AUTHORIZED')
        result=workflow_engine.execute_gate(workflow_id,'decision.execute',actor,True,idempotency_key=decision_id); d.status=DecisionStatus.EXECUTED; return result
    def override(self,decision_id,actor,reason,new_decision):
        d=self.decisions[decision_id]; r={'decision_id':decision_id,'actor':actor,'reason':reason,'timestamp':time(),'previous_decision':d.decision,'new_decision':new_decision}; self.overrides.append(r); d.decision=new_decision; return r
    def journal_entry(self,decision_id,**fields):
        j={'decision_id':decision_id,**fields}; self.journal.append(j); return j
    def effectiveness(self,decision_id,expected,actual):
        if expected is None or actual is None:return {'decision_id':decision_id,'status':'NO_DATA'}
        if not isinstance(expected,(int,float)) or not isinstance(actual,(int,float)):return {'decision_id':decision_id,'status':'UNKNOWN'}
        return {'decision_id':decision_id,'status':'MEASURED','expected':expected,'actual':actual,'prediction_error':actual-expected}
    def disagreement(self,analyses):
        if not analyses:return 'UNKNOWN'
        recommendations={a.get('recommendation') for a in analyses}
        return 'AGREEMENT' if len(recommendations)==1 else 'DISAGREEMENT'
    def knowledge_trace(self,reference,freshness,provenance,confidence,scope,limitations=None): return {'reference':reference,'freshness':freshness,'provenance':provenance,'confidence':confidence,'scope':scope,'limitations':limitations or []}
    def decision_learning(self,prediction,actual,reason): return {'prediction':prediction,'actual':actual,'prediction_error':None if prediction is None or actual is None else actual-prediction,'reason':reason,'evidence':'INFERRED'}
