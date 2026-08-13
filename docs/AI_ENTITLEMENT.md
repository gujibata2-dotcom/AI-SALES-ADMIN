# AI Entitlement

Every customer operation must resolve tenant → plan → entitlement → authorization before execution. Limits include employees, tasks, knowledge, storage and tool access. Entitlement decisions are server-side and tenant-scoped.

Upgrade and downgrade policy belongs above this domain primitive; downgrade must not silently delete customer data.
