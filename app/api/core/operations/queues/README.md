# Queue Management

Queues: SALES_QUEUE, ADMIN_QUEUE, SUPPORT_QUEUE, ESCALATION_QUEUE, APPROVAL_QUEUE, KNOWLEDGE_REVIEW_QUEUE.

Queue records contain priority, created_at, status, assignment and retry_count. Scheduling must prevent starvation of low-priority tasks; priority never pressures customers.