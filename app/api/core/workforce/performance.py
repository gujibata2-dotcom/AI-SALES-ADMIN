"""Team performance contracts. Real production scores are NOT fabricated."""
METRICS=('completion_rate','quality','accuracy','latency','cost','reliability','rework_rate','handoff_quality','conflict_rate','recovery_rate')

def compare_modes(single:dict, multi:dict)->str:
    if not single or not multi:return 'NOT_EVALUATED'
    if multi.get('quality',0)>single.get('quality',0) and multi.get('reliability',0)>=single.get('reliability',0):return 'MULTI_AGENT'
    return 'SINGLE_AGENT'
