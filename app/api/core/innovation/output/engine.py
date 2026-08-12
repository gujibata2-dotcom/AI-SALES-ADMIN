def release_readiness(technical: bool, operational: bool, security: bool, documentation: bool, monitoring: bool, rollback: bool) -> dict:
    ready=all((technical,operational,security,documentation,monitoring,rollback))
    return {"status":"PRODUCTION_READY" if ready else "NOT_READY","rollback_required":not rollback}
