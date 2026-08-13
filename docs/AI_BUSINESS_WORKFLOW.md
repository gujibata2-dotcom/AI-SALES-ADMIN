# AI Business Workflow

Workflows are durable records containing context, decisions, tasks, outputs, errors, approvals, artifacts, events and outcomes. State transitions are explicit; invalid jumps are rejected.

Supported states include CREATED, QUEUED, RUNNING, WAITING, BLOCKED, REVIEW_REQUIRED, PAUSED, FAILED, RECOVERING, COMPLETED and CANCELED.

Pause/resume preserves state. External actions should use idempotency keys. Event triggers are recorded with condition results.
