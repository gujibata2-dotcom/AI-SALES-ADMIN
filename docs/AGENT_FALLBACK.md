# Agent Fallback

Retry only transient timeout/provider/rate-limit failures and always obey max_retries. Provider/agent health is bounded by the Phase 25 circuit-breaker model. Reversible failures may rollback; irreversible side effects stop and escalate. Fallback must be approved and re-authorized.
