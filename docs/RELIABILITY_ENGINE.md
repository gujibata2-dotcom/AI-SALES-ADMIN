# Phase 25 — Reliability Engine

`Observe → Detect → Diagnose → Assess → Recover → Verify → Escalate → Report → Learn`

Bounded self-healing only: retry, restart, pause/resume, approved fallback, reassign, rollback and escalation. It cannot modify governance, permissions, security, audit or kill switches.

Health evidence is authoritative; insufficient evidence produces `UNKNOWN`. Health checks are side-effect free. All recovery is authorized and bounded by attempts, timeout, backoff and scope.

Phase 25 consumes Phase 24 execution/verification outcomes and emits incident, recovery, failure and human-correction events for Phase 12 learning. Production integrations and real side effects are intentionally absent.
