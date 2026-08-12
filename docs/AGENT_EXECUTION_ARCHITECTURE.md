# Phase 27 Agent Execution Architecture

Employee, Model, Agent and Tool are separate abstractions. The execution path is: understand → plan → model route → agent/tool selection → authorize → prepare → execute → verify → monitor → recover → report.

All external side effects pass authorization and policy gates. Providers are adapters only. No provider API is called directly by business logic. Manus is an optional provider and is represented only by contracts/mocks in this phase.

Limits include max steps, depth, retries, agent calls, action count, cost and execution time. HIGH/CRITICAL side effects require explicit human approval when policy says HUMAN_REQUIRED. DRY_RUN and SIMULATE never create external side effects.