# AI Employee Usage

`UsageMeter` records organization, employee/task context, resource type, quantity and timestamp. `QuotaEngine` derives `AVAILABLE`, `WARNING` (80%+), `LIMITED` (100%) and `EXCEEDED` states.

Quota consumption is checked before recording usage, preventing accidental overage in the local service boundary. Additional paid usage is intentionally not implemented; a future billing adapter must require explicit authorization.
