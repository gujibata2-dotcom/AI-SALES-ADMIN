"""Failure recovery policy for multi-employee execution."""
RETRYABLE = {"TRANSIENT_FAILURE", "TIMEOUT", "TEMPORARY_PROVIDER_FAILURE"}
ESCALATE = {"POLICY_CONFLICT", "SECURITY", "LEGAL", "FINANCIAL", "IRREVERSIBLE", "UNRESOLVED_CONFLICT"}

def recover(failure, primary, backup=None):
    if failure in RETRYABLE: return "RETRY"
    if backup and failure not in ESCALATE: return f"FALLBACK:{backup}"
    return "HUMAN_ESCALATION"
