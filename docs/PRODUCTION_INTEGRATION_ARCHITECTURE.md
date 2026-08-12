# Production Integration Architecture

Phase 28 adds a governed external-system boundary. Runtime flow is:
Employee → Model Router → Agent Router → Tool → Integration Gate → Outbox → Provider Adapter → Verify → Reliability → Learning.

External side effects are never exposed directly to business logic. Provider adapters implement the common contract and receive only credential references resolved by secret management.

Production deployment requires Phase 19 governance approval, Phase 24 bounded authorization, Phase 25 health/recovery controls, Phase 26 model routing, and Phase 27 agent/tool authorization.
