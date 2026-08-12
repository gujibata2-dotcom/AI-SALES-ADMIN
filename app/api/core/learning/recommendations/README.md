# Improvement Recommendations

Supported types:
- KNOWLEDGE_UPDATE
- FAQ_UPDATE
- RETRIEVAL_UPDATE
- PROMPT_UPDATE
- RESPONSE_POLICY_UPDATE
- WORKFLOW_UPDATE
- SALES_POLICY_UPDATE
- CLARIFICATION_UPDATE

Required fields:
- recommendation_id
- type
- problem
- evidence
- proposed_change
- expected_benefit
- risk
- affected_components
- requires_human_approval

Every recommendation is a proposal. Human approval is mandatory for knowledge, prompts, workflows, sales policies, and retrieval ranking changes. The AI cannot approve its own recommendation.
