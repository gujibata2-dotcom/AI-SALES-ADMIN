# Disaster Recovery

Phase 25 defines contracts for recovery point, recovery time, backup/restore ownership, safe checkpointing and restoration verification. It does not create production backups.

Workflow recovery uses safe checkpoints. After restart, the system verifies checkpoint validity and idempotency before repeating any action. Failed retries enter a dead-letter state with context, error and audit preserved for human recovery.
