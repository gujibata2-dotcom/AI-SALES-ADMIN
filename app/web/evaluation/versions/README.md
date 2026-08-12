# Governance approvals, versions, risk, audit

Approval states are explicit and append-only. A human must approve HIGH and CRITICAL changes; AI cannot approve its own recommendation.

Version records are immutable after approval. Versioned types: prompt, policy, knowledge, workflow, agent config, evaluation criteria, and content rules.

Risk classification is LOW, MEDIUM, HIGH, CRITICAL. CRITICAL includes financial, legal, privacy, security, customer harm, and irreversible actions.

Audit entries are append-only and trace who/what/why/when/risk/evaluation/approval/deployment/rollback. AI cannot modify audit history, escalate privileges, bypass policy, or disable safety gates.