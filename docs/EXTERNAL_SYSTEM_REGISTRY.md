# External System Registry

Systems declare provider, category, capabilities, allowed operations, approval requirements, rate limits and webhook support.

Credentials are represented only by `credential_reference`; secrets must live in environment/secret management.

Operations are least-privilege: READ, WRITE, SEND, PUBLISH, DELETE, ADMIN. A business role never receives unrestricted platform access.
