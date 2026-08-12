# Governance — Phase 19

Governance controls prompts, policies, knowledge, workflows, response behavior, sales behavior, content, multilingual behavior, social behavior, agent configuration, and learning recommendations.

## Risk
LOW: automated validation. MEDIUM: review recommended. HIGH: human approval. CRITICAL: mandatory human approval. Critical includes financial, legal, privacy, security, customer-harm, and irreversible actions.

## Approval invariant
AI cannot approve its own change. Approval requires a human actor distinct from the proposing/evaluating agent. Rejection or missing approval prevents versioning and release.

## Immutable versioning
Approved objects are immutable. A change creates a new version with parent_version, creator, reason, approval, timestamp, and status.

Audit records must capture who, what, why, when, risk, evaluation, approval, deployment, and rollback. Audit history cannot be modified by the AI Employee.
