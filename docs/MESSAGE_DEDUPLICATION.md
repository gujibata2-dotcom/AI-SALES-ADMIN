# Message Deduplication

Use message_id, idempotency_key and conversation_reference to prevent duplicate response, follow-up, task creation and webhook processing. Duplicate requests are deduplicated, never blindly replayed.