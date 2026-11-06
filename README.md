# ContentOS

### Engineering AI-native workflows beyond a single prompt

ContentOS is a runnable public reference implementation for coordinating AI workers, structured artifacts, task state, and human approvals across a multi-stage content workflow.

> Building AI features is one thing. Building a system that coordinates AI, people, tasks, and decisions reliably is a different engineering challenge.

This repository is intentionally generic and uses synthetic data. It does not contain private company names, private records, credentials, or claims about a proprietary production system.

## What is implemented

- A FastAPI service exposing workflow, task, artifact, and event data.
- A deterministic mock orchestration engine that creates a content-production workflow from a brief.
- Explicit task states: `queued`, `running`, `needs_review`, `approved`, `failed`.
- Replaceable worker interfaces for planning, slides, reading material, quizzes, and validation.
- A browser dashboard for inspecting execution state and approving or requesting revision.
- Tests for workflow creation, state transitions, and API behavior.

## Reference workflow

```text
Brief
  -> Requirements & planning
  -> Parallel artifact workers
  -> Artifact validation
  -> Human review
  -> Approved output
```

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000.

The demo works without an API key. To create a new workflow from the API:

```bash
curl -X POST http://127.0.0.1:8000/api/workflows \
  -H "Content-Type: application/json" \
  -d '{"title":"Intro to feedback loops","audience":"Early-career engineers","deliverables":["slides","reading_material","quiz"]}'
```

## Engineering decisions

### Why not one giant agent?

Isolated tasks are easier to validate, retry, debug, and measure. ContentOS treats orchestration and inference as separate concerns.

### Why a deterministic mock model?

The public repository must be runnable and testable without vendor accounts or model credentials. A model adapter can be added later without changing workflow state or the dashboard.

### Why make approval explicit?

Generated output is not automatically production-ready. Approval is a responsibility with a visible state transition, not an implicit side effect of generation.

## Repository map

```text
app/
  main.py              # FastAPI routes and static file hosting
  models.py            # API and domain schemas
  orchestrator.py      # Workflow state machine and mock workers
  static/              # Dashboard UI
tests/                 # API and workflow tests
docs/                  # Architecture and workflow notes
```

## Status

**Public reference implementation — v0.1.**

The code in this repository is implemented and runnable. Provider-backed model execution, durable persistence, authentication, and multi-user concurrency are planned extensions, not current capabilities.

## License

MIT
