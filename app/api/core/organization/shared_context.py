"""Shared context isolation rules."""
SCOPES = ("PUBLIC_CONTEXT", "TEAM_CONTEXT", "EMPLOYEE_CONTEXT", "SENSITIVE_CONTEXT")

def can_share(source_scope: str, target_scope: str, authorized: bool) -> bool:
    if source_scope == "SENSITIVE_CONTEXT" and not authorized: return False
    return authorized or (source_scope == target_scope == "PUBLIC_CONTEXT")
