# Rollback Policy

Rollback is attempted only for reversible actions. Each rollback records reason, trigger, original action, rollback/compensating action and result. Irreversible operations require a compensating action when possible; otherwise the system stops and escalates to a human.
