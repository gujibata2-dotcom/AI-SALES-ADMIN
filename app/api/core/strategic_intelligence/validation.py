"""Deterministic Phase 40 validation helpers."""
from typing import Any

REQUIRED_FORECAST=('forecast_id','target','prediction','time_horizon','assumptions','evidence','confidence','uncertainty','limitations')
REQUIRED_SIGNAL=('signal_id','source','signal_type','observation','timestamp','domain','relevance','quality','confidence','provenance','limitations')

def validate_required(record:dict[str,Any], fields:tuple[str,...])->list[str]: return [f'missing:{f}' for f in fields if f not in record]
def validate_score(value:Any,name:str)->list[str]:
    return [] if isinstance(value,(int,float)) and 0<=value<=1 else [f'invalid:{name}']
def validate_signal(record:dict[str,Any])->list[str]:
    e=validate_required(record,REQUIRED_SIGNAL)
    for k in ('relevance','quality','confidence'): e += validate_score(record.get(k),k)
    if not record.get('provenance'): e.append('missing:provenance')
    return e
def validate_forecast(record:dict[str,Any])->list[str]:
    e=validate_required(record,REQUIRED_FORECAST)+validate_score(record.get('confidence'),'confidence')
    if not record.get('assumptions'): e.append('missing:assumptions')
    if not record.get('evidence'): e.append('missing:evidence')
    return e
def uncertainty_label(confidence:float, contested:bool=False)->str:
    if contested:return 'CONTESTED'
    if confidence < .4:return 'UNKNOWN'
    if confidence < .75:return 'UNCERTAIN'
    return 'ESTIMATED'
def require_human_review(impact:float,risk:float,irreversible:bool,uncertain:bool)->bool:
    return irreversible or impact>=.8 or risk>=.8 or uncertain
