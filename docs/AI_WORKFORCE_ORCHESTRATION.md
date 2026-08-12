# AI Workforce Orchestration
Phase 33 introduces a policy-bounded workforce layer over Phases 26, 30, 31 and 32.

Flow: Task → complexity/risk → single agent or team → DAG → assignment → execute → independent review → verify → deliver → evaluate → learn.

The workforce layer does not grant permissions. It consumes existing authorization/governance contracts. Team composition is evidence- and capability-driven, not role-name-driven. If a single employee satisfies the task safely, the engine should prefer SINGLE_AGENT to avoid coordination cost.

Critical actions require independent review and, where policy demands, human approval. Production integrations remain outside this phase unless an existing contract exists.