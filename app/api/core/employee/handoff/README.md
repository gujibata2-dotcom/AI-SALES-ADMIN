# Collaboration, delegation and handoff

Supported: AI → AI, AI → Human, Human → AI, and interaction with authorized external services through existing gateways.

Delegation checks skill, permission, risk, availability, workload, and governance. The executor's own permission is authoritative; no permission propagation occurs.

Handoff payload must contain: task_id, context, work_done, pending_work, customer_need, known_facts, unknowns, risk, recommended_next_action.

Share only approved knowledge, task context, workflow state, and non-sensitive business context. Do not share unnecessary PII, private credentials, secrets, or restricted information.

Structured messages use the Phase 21 collaboration schema. High-risk, uncertain, complaint, security, legal, financial, privacy, or policy-conflict work escalates to humans.