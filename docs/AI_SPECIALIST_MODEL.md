# Specialist model

A specialist has `domain`, `expertise`, `knowledge_sources`, `confidence`, `limitations`, and `escalation_rules`.

Example domains: Automotive, Real Estate, Travel, Product, Customer Support, Content.

Specialists use Phase 3 Knowledge Engine: Question → Knowledge Retrieval → Source Verification → Answer.

If knowledge is unavailable or uncertain: `UNKNOWN`; do not guess, fabricate specification, price, stock, or other product facts.

Specialist cannot override Core Ethics, Governance, Authorization, Safety, Privacy, or Audit controls.