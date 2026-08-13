"""Phase 40 registries: append-only history for forecasts, scenarios and decisions."""
from dataclasses import dataclass,field
from typing import Any
@dataclass
class VersionedRegistry:
    current:dict[str,Any]=field(default_factory=dict)
    history:dict[str,list[Any]]=field(default_factory=dict)
    def put(self,key:str,value:Any):
        self.current[key]=value; self.history.setdefault(key,[]).append(value)
    def versions(self,key:str): return tuple(self.history.get(key,()))
@dataclass(frozen=True)
class StrategicDecision:
    decision_id:str; context:str; options:list[str]; selected_option:str|None; reason:str
    evidence:list[str]; assumptions:list[str]; risk:list[str]; expected_outcome:str; actual_outcome:str|None=None

def decision_quality(expected:str,actual:str,decision_quality_known:bool=True)->str:
    if not decision_quality_known:return 'UNKNOWN'
    good_outcome=actual=='SUCCESS'; good_decision=expected=='SOUND'
    if good_decision and good_outcome:return 'GOOD_DECISION_GOOD_OUTCOME'
    if good_decision:return 'GOOD_DECISION_BAD_OUTCOME'
    if good_outcome:return 'BAD_DECISION_GOOD_OUTCOME'
    return 'BAD_DECISION_BAD_OUTCOME'
