# Business Rule Engine

Business rules are separate from the AI model and cannot be changed through prompts.

Rule types: `PRICE_RULE`, `DISCOUNT_RULE`, `STOCK_RULE`, `RETURN_RULE`, `WARRANTY_RULE`, `DELIVERY_RULE`, `ESCALATION_RULE`.

Each rule requires `rule_id`, `description`, `status`, `priority`, `scope`, `source`, `effective_from`, `effective_until`, and `approval_required`.

The model may evaluate rules but cannot authoritatively modify them.