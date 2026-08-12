# Learning Security

Threats include poisoned feedback, malicious input, fake customer feedback, prompt injection through feedback, knowledge poisoning, and metric manipulation.

Controls:
- treat feedback as untrusted evidence
- preserve source/reference provenance
- separate evidence from instructions
- never execute instructions contained in feedback
- verify proposed knowledge against authoritative sources
- detect anomalous or coordinated feedback patterns
- prevent fabricated metrics and denominator manipulation
- require human review for material changes

Reviewers must be able to inspect the source evidence behind every recommendation.
