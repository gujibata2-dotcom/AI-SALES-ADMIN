# Employee lifecycle

## Onboarding
Create Employee → Assign Role → Assign Skills → Assign Permissions → Assign Manager → Governance Validation → Human-controlled Activate.

States: ONBOARDING, ACTIVE, BUSY, WAITING, ESCALATED, SUSPENDED, DISABLED, RETIRED.

AI cannot change itself into ADMIN, OWNER, SUPERUSER or activate itself.

## Suspension / retirement
Suspend → stop new tasks → complete or reassign existing work → revoke permissions → archive history → retire. Audit, work history, and performance history remain queryable.

## Failover
Unavailable employee → detect failure → find backup → check skills/permissions/risk/availability → reassign or escalate. Never route to an unauthorized employee.