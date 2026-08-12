INCIDENT_STAGES = ("DETECT", "CONTAIN", "INVESTIGATE", "RECOVER", "VERIFY", "REPORT", "LEARN")
def incident_event(incident_id: str, stage: str) -> dict:
    if stage not in INCIDENT_STAGES: raise ValueError("invalid incident stage")
    return {"incident_id": incident_id, "stage": stage, "status": "NOT_EVALUATED"}
