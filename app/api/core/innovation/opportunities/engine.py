def prioritize(dimensions: dict) -> dict:
    keys = ("impact","feasibility","cost","risk","strategic_alignment","time","evidence")
    return {"dimensions": {k: dimensions.get(k, "UNKNOWN") for k in keys}, "composite_score": None}
