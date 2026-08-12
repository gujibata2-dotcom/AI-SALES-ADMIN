# Verification

Statuses: ACTION_ACCEPTED, ACTION_EXECUTED, ACTION_FAILED, ACTION_PARTIALLY_COMPLETED, ACTION_RESULT_UNKNOWN.

`EXECUTED ≠ SUCCESSFUL`. Verification must inspect the adapter result. Unknown results must not be represented as success.