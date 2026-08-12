# Action Model

Action types: READ, SEARCH, ANALYZE, RECOMMEND, REQUEST_INFORMATION, PREPARE, SEND, UPDATE, CREATE, CANCEL, ESCALATE.

Risk levels: LOW, MEDIUM, HIGH, CRITICAL.

Examples: READ_PRODUCT=LOW, PREPARE_ORDER=MEDIUM, SEND_MESSAGE=MEDIUM, CHANGE_PRICE=HIGH, REFUND_PAYMENT=CRITICAL.

Risk is determined by side effect, reversibility, financial/legal impact, privacy impact, and customer impact. Critical actions are blocked in Phase 10.