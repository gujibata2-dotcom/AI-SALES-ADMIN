# AI Employee Subscriptions

Subscription states: `TRIAL`, `ACTIVE`, `PAST_DUE`, `PAUSED`, `CANCELED`, `EXPIRED`, `UNKNOWN`.

Trial creation is local state. Activation requires explicit payment authorization and a billing adapter that returns `ACTIVE`. The default adapter returns `BILLING_NOT_CONFIGURED` and cannot produce fake payment success.

Package changes are authorization-protected and downgrade checks employee limits before changing the subscription. Cancellation records retention state rather than deleting tenant data.
