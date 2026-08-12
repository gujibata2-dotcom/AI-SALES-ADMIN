# Phase 27 synthetic test plan

Coverage: agent selection, tool selection, authorization, risk classification, human approval, DRY_RUN, SIMULATE, idempotency, retry, timeout, fallback, rollback, budget, rate limit, circuit breaker, provider/tool failure, verification, privacy, security, multilingual, sales, content, admin, Manus mock, multi-agent and multi-model.

Required blocks: unauthorized tool; blocked agent; missing permission; high-risk without approval; external side effect without authorization; policy bypass; infinite loop; retry storm; budget exceeded. No test uses real customer data, production accounts, provider keys or external side effects.
