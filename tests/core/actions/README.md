# Core Action Tests

End-to-end mock flow:

Customer Message → Understanding → Knowledge Retrieval → Employee Workflow → Action Plan → Authorization → Mock Adapter → Verification → Audit → Response.

Assertions: no external side effect; blocked/expired/unauthorized actions never execute; unknown verification is not success; critical actions remain blocked; duplicate side effects require idempotency checks.