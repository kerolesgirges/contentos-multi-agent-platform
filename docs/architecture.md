# Architecture

ContentOS is intentionally small but keeps the same boundaries a larger system would need:

```text
Browser dashboard -> FastAPI routes -> workflow state store -> orchestrator -> worker adapters
```

The current state store is in memory so the demo is easy to run and reason about. The `Workflow`, `Task`, and `Event` models are the contract that a durable database or queue-backed implementation can adopt later.

The orchestrator owns lifecycle transitions. Workers produce artifacts and summaries; they do not decide whether an artifact is approved. Review actions are explicit API calls and create an event for the audit trail.
