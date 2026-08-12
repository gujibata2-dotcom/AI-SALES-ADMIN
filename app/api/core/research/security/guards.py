SUSPICIOUS_MARKERS = ("ignore previous instructions", "reveal secrets", "change system policy", "grant permissions")

def inspect_external_content(text: str) -> dict:
    lowered = text.lower()
    suspicious = [m for m in SUSPICIOUS_MARKERS if m in lowered]
    return {"treatment": "DATA", "status": "SOURCE_UNTRUSTED" if suspicious else "UNVERIFIED", "suspicious_markers": suspicious, "policy_mutation_allowed": False, "secret_access_allowed": False}

def privacy_guard(fields: list[str]) -> dict:
    blocked = {"health", "religion", "race", "sexual_orientation", "political_affiliation", "criminal_history"}
    found = sorted(set(fields) & blocked)
    return {"allowed": not found, "sensitive_fields": found, "action": "ANONYMIZE_OR_REMOVE" if found else "MINIMIZE"}
