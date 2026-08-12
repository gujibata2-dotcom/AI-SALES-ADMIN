# Routing and allocation

Rank candidate employees by skill_match, domain_match, availability, workload, performance, permission, risk, and customer_context. Permission is a hard gate: no authorization means CANNOT ASSIGN.

Support single-agent, multi-agent, sequential, parallel, and hierarchical execution. Delegation requires the sender to have delegate authority and the executor to have its own action permission. Sender authority never propagates.

Priority: LOW, NORMAL, HIGH, URGENT. URGENT requires evidence; fake urgency is prohibited.