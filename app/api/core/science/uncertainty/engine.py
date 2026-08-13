"""Uncertainty and belief updates; probabilities are never fabricated."""

def uncertainty(measurement=None, model=None, data=None, parameter=None, knowledge=None) -> dict:
    return {"MEASUREMENT_UNCERTAINTY":measurement,"MODEL_UNCERTAINTY":model,"DATA_UNCERTAINTY":data,"PARAMETER_UNCERTAINTY":parameter,"KNOWLEDGE_UNCERTAINTY":knowledge}

def belief_update(prior_assumption, evidence, posterior=None, reason="") -> dict:
    if posterior is None:
        return {"status":"UNKNOWN","prior_assumption":prior_assumption,"evidence":evidence,"update_reason":reason}
    return {"prior_assumption":prior_assumption,"evidence":evidence,"posterior":posterior,"update_reason":reason}
