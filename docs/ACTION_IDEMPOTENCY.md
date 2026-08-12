# Idempotency

All future side-effecting actions require an `idempotency_key`. It prevents duplicate messages, orders, updates, and payments.

An action must not execute again until its idempotency state is checked.