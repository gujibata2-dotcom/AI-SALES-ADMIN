# Pattern Detection

Patterns may include repeated questions, product/FAQ knowledge gaps, retrieval misses, translation issues, clarification loops, objection patterns, workflow bottlenecks, escalation patterns, and action failures.

Every pattern must contain:
- pattern_id
- description
- evidence_count
- source_events
- confidence
- time_range
- limitations

Minimum evidence thresholds must be configured by the owning evaluation policy. The engine must not generalize from tiny samples, convert correlation to causation, or infer sensitive attributes.
