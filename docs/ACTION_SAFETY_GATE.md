# Action Safety Gate

Every action passes:

`Intent Check → Knowledge Check → Business Rule Check → Authorization Check → Privacy Check → Risk Check → Execution → Verification → Audit`

Any failed gate results in BLOCK or HUMAN_APPROVAL. No workflow may bypass this gate.