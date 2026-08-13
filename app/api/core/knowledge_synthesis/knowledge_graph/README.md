# Knowledge Graph

Graph nodes retain entity, claim, knowledge, principle and application provenance. Relationships are typed: `supports`, `contradicts`, `depends_on`, `causes`, `related_to`, `derived_from`, `supersedes`, `applies_to`.

Every mutation records graph version, change, reason, source, timestamp and review. Historical graph state is never deleted. Traversals that discover indirect links must label the result `INFERRED` and expose supporting edges.