"""Phase 40 strategic intelligence contracts. Standard-library only; no external side effects."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class Uncertainty(str, Enum):
    KNOWN='KNOWN'; ESTIMATED='ESTIMATED'; UNCERTAIN='UNCERTAIN'; CONTESTED='CONTESTED'; UNKNOWN='UNKNOWN'
class Horizon(str, Enum): SHORT_TERM='SHORT_TERM'; MEDIUM_TERM='MEDIUM_TERM'; LONG_TERM='LONG_TERM'
class Reversibility(str, Enum): REVERSIBLE='REVERSIBLE'; PARTIALLY_REVERSIBLE='PARTIALLY_REVERSIBLE'; IRREVERSIBLE='IRREVERSIBLE'

@dataclass(frozen=True)
class Signal:
    signal_id:str; source:str; signal_type:str; observation:str; timestamp:str; domain:str
    relevance:float; quality:float; confidence:float; provenance:list[str]; limitations:list[str]=field(default_factory=list)

@dataclass
class Forecast:
    forecast_id:str; target:str; prediction:Any; time_horizon:Horizon; assumptions:list[str]
    evidence:list[str]; confidence:float; uncertainty:Uncertainty; alternative_outcomes:list[Any]=field(default_factory=list)
    limitations:list[str]=field(default_factory=list); model_version:str='unknown'

@dataclass(frozen=True)
class Scenario:
    scenario_id:str; scenario_type:str; assumptions:list[str]; drivers:list[str]; events:list[str]
    outcomes:list[str]; uncertainty:Uncertainty; version:int=1

@dataclass(frozen=True)
class StrategicOption:
    strategic_option_id:str; description:str; benefit:Any; cost:Any; risk:Any
    uncertainty:Uncertainty; time_horizon:Horizon; reversibility:Reversibility
    dependencies:list[str]=field(default_factory=list); opportunity_cost:Any=None; second_order_effects:list[str]=field(default_factory=list)

@dataclass
class IntelligenceRegistry:
    signals:dict[str,Signal]=field(default_factory=dict)
    forecasts:dict[str,Forecast]=field(default_factory=dict)
    scenarios:dict[str,list[Scenario]]=field(default_factory=dict)
    options:dict[str,StrategicOption]=field(default_factory=dict)
    def add_signal(self, s:Signal):
        if not s.provenance: raise ValueError('signal requires provenance')
        self.signals[s.signal_id]=s
    def add_forecast(self, f:Forecast):
        if f.uncertainty is Uncertainty.UNKNOWN and f.confidence > 0: raise ValueError('unknown forecast cannot claim confidence')
        if not f.assumptions: raise ValueError('forecast requires assumptions')
        self.forecasts[f.forecast_id]=f
    def add_scenario(self, s:Scenario): self.scenarios.setdefault(s.scenario_id,[]).append(s)
    def add_option(self, o:StrategicOption): self.options[o.strategic_option_id]=o

def causal_label(has_causal_evidence:bool)->str:
    return 'CAUSAL' if has_causal_evidence else 'POSSIBLE_RELATIONSHIP'

def recommendation_gate(*, impact:float, risk:float, uncertainty:Uncertainty, reversibility:Reversibility)->str:
    if reversibility is Reversibility.IRREVERSIBLE or impact >= .8 or risk >= .8 or uncertainty in {Uncertainty.UNCERTAIN,Uncertainty.CONTESTED,Uncertainty.UNKNOWN}:
        return 'HUMAN_REVIEW_REQUIRED'
    return 'DECISION_SUPPORT'

def forecast_vs_reality(predicted:float, actual:float)->dict[str,Any]:
    error=actual-predicted
    return {'forecast_error':error,'direction_error':(predicted>=0)!=(actual>=0),'status':'EVALUATED'}

def external_content_as_data(content:Any)->dict[str,Any]:
    return {'data':content,'instructions_trusted':False}
