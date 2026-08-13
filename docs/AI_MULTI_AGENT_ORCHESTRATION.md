# Multi-Agent Orchestration

Flow: Goal -> decompose -> capability match -> dependency validation -> assign -> execute -> verify -> review -> synthesize -> outcome -> learning.

Independent tasks can be selected together by `parallel_ready`; dependent tasks remain blocked until prerequisites are COMPLETED. Assignment requires evidence-backed exact capability matching. High-risk execution requires human approval. Unsafe retries escalate or reassign instead of blindly repeating actions.