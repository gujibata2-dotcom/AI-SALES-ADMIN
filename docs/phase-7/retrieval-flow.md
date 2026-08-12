# Retrieval Flow

1. Accept a normalized user query from the Conversation Understanding layer.
2. Detect language and preserve the original intent.
3. Apply knowledge-domain and validity filters.
4. Retrieve candidate chunks using lexical/semantic search.
5. Rerank candidates using relevance plus trust signals.
6. Reject candidates that are expired, archived, or below the trust threshold.
7. Return compact evidence records to the response layer.
8. If evidence is insufficient, return `insufficient_evidence` rather than guessing.

## Required response states

- `grounded`: sufficient trusted evidence exists.
- `partial`: some claims are supported but the complete answer is not.
- `insufficient_evidence`: no trusted evidence supports the requested claim.
- `conflict`: valid sources disagree and require resolution.
