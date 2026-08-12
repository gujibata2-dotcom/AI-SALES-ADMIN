from typing import Dict, Any

def utilization(used, capacity):
    if used is None or capacity in (None, 0):
        return {"status": "NOT_PROVIDED", "utilization": None}
    return {"status": "KNOWN", "utilization": used / capacity}

def detect_waste(metrics: Dict[str, Any]) -> list[str]:
    alerts = []
    if metrics.get("unused_resources", 0): alerts.append("LOW_UTILIZATION")
    if metrics.get("duplicate_usage", 0): alerts.append("DUPLICATE_USAGE")
    if metrics.get("excessive_retries", 0): alerts.append("HIGH_REWORK")
    return alerts
