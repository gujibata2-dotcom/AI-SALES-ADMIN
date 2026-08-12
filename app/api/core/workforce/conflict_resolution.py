"""Conflict resolution primitives; never resolve by vote alone."""
CONFLICT_TYPES={'FACT_CONFLICT','INTERPRETATION_CONFLICT','STRATEGY_CONFLICT','POLICY_CONFLICT','DATA_CONFLICT','TOOL_RESULT_CONFLICT','PERMISSION_CONFLICT'}

def classify(conflict_type:str)->str:
    return conflict_type if conflict_type in CONFLICT_TYPES else 'DATA_CONFLICT'

def resolve_strategy(results:list[dict])->dict:
    # Evidence quality and specialization outrank agreement count.
    ranked=sorted(results,key=lambda r:(r.get('evidence_quality',0),r.get('specialization',0),r.get('confidence',0)),reverse=True)
    if not ranked:return {'status':'ESCALATE','reason':'NO_RESULTS'}
    top=ranked[0]
    if len(ranked)>1 and top.get('evidence_quality',0)==ranked[1].get('evidence_quality',0) and top.get('confidence',0)==ranked[1].get('confidence',0):
        return {'status':'ESCALATE','reason':'UNRESOLVED_EQUAL_EVIDENCE'}
    return {'status':'RECOMMENDATION','result':top.get('result')}
