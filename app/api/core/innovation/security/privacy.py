def privacy_guard(fields: list[str]) -> dict:
    sensitive={"health","biometric","religion","sexual_orientation","political_opinion"}
    hits=[f for f in fields if f in sensitive]
    return {"allowed":not hits,"sensitive_fields":hits,"status":"BLOCKED" if hits else "ALLOWED"}
