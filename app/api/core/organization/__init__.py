"""Phase 30 collective intelligence engine boundaries."""

AUTHORITY = ("EMPLOYEE", "TEAM", "COORDINATOR", "GOVERNANCE", "HUMAN")
STATUS = ("TRAINING", "ACTIVE", "PAUSED", "SUSPENDED", "REVIEW", "RETIRED")
TASK_STATUS = ("PENDING", "READY", "RUNNING", "WAITING", "BLOCKED", "REVIEW", "DONE", "FAILED", "CANCELLED")


def require_permission(granted: set[str], required: str) -> None:
    if required not in granted:
        raise PermissionError(f"BLOCK: missing permission {required}")


def bounded_delegation(scope: set[str], allowed: set[str], risk: str) -> bool:
    return scope <= allowed and risk in {"LOW", "MEDIUM"}
