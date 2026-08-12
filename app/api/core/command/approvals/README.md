# Business Command Center

The command plane aggregates business health, priorities, risks, opportunities, active decisions, approvals, team status, customer/sales/support/content/knowledge signals, and incidents.

Human controls: approve, reject, request more information, choose option, modify plan, defer, cancel, pause, prioritize, rollback. Critical actions are protected by RBAC and authorization.

Incident deduplication uses correlation_id + event fingerprint + time window. Alerts are severity-ranked and rate-limited to avoid alert spam.
