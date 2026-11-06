# ContentOS

### A reference implementation for observable, human-supervised AI workflows

[![Python](https://img.shields.io/badge/Python-3.10%2B-1f4b73?style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-0f766e?style=flat-square)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-3%20passing-2f855a?style=flat-square)](#testing)
[![License](https://img.shields.io/badge/license-MIT-6b7280?style=flat-square)](LICENSE)

ContentOS is a small but complete public reference implementation for coordinating AI-assisted content production as a traceable workflow.

It demonstrates how a system can move from a brief to structured artifacts while keeping task state, execution history, confidence, and human approval visible at every important boundary.

> I am less interested in building an agent that sounds intelligent than in building a workflow that can explain what happened, recover from uncertainty, and give a human the right decision at the right time.

This is a generic portfolio project. It uses synthetic data and deterministic mock workers. It contains no private company information, user records, API keys, or proprietary source code.

## Why this project exists

Many AI demos stop at a prompt and a response. Real operational systems need more:

- explicit task ownership and lifecycle state;
- structured intermediate artifacts;
- validation before approval;
- event history for debugging and trust;
- clear boundaries between automation and human judgment.

ContentOS focuses on those boundaries. The implementation is intentionally compact so the design can be inspected without a large framework or infrastructure setup.

## What is implemented

| Area | Current implementation |
| --- | --- |
| API | FastAPI routes for health, workflow creation, retrieval, and task review |
| Workflow state | `queued`, `running`, `needs_review`, `approved`, and `failed` |
| Orchestration | Deterministic workflow creation with planning, deliverable, and validation tasks |
| Review | Approve or request revision with a persisted review note and event |
| Observability | Workflow events, task owners, runtime values, confidence, and artifact IDs |
| UI | Responsive browser dashboard for task inspection and review actions |
| Data | Synthetic, in-memory state; no API key required |
| Verification | API tests covering health, creation, review transitions, and 404 behavior |

## System overview

```text
┌─────────────┐     ┌─────────────┐     ┌────────────────┐
│ Browser UI  │────▶│ FastAPI API │────▶│ Orchestrator   │
└─────────────┘     └─────────────┘     └───────┬────────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         ▼                      ▼                      ▼
                   Planner task          Artifact tasks          Validation task
                         │                      │                      │
                         └──────────────────────┴──────────────────────┘
                                                │
                                       Human review checkpoint
                                                │
                                      Approval or revision
```

The current store is in memory by design. `Workflow`, `Task`, and `Event` are explicit domain contracts so a later version can replace the store with a database or queue-backed runtime without changing the dashboard's core interaction model.

## Quickstart

### 1. Create an environment

```bash
python -m venv .venv
```

Activate it:

```powershell
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the application

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the dashboard.

FastAPI's generated API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Try the API

Create a synthetic workflow:

```bash
curl -X POST http://127.0.0.1:8000/api/workflows \
  -H "Content-Type: application/json" \
  -d '{"title":"Intro to feedback loops","audience":"Early-career engineers","deliverables":["slides","reading_material","quiz"]}'
```

The response contains a workflow ID, task list, and event history. Find a task whose state is `needs_review`, then submit a decision:

```bash
curl -X POST http://127.0.0.1:8000/api/workflows/<workflow_id>/tasks/<task_id>/review \
  -H "Content-Type: application/json" \
  -d '{"decision":"approve","note":"Aligned to the stated objectives."}'
```

The review call changes the task state, records the note, creates an event, and recalculates the workflow state.

## Testing

Run the test suite with:

```bash
python -m pytest -q
```

The tests currently cover:

- health endpoint availability;
- workflow creation from a validated brief;
- transition from `needs_review` to `approved`;
- missing workflow handling with a `404` response.

## Engineering decisions

### Orchestration is separate from inference

The orchestrator owns task lifecycle and review transitions. A model provider should produce an artifact or structured result; it should not silently decide whether that result is approved.

### Deterministic workers make the demo reproducible

This repository needs to be runnable by a reviewer without vendor credentials or a paid model account. The mock runtime makes the workflow behavior predictable while leaving room for provider adapters later.

### Review is a state transition, not a UI decoration

`needs_review` exists in the domain model, API behavior, dashboard, and event history. The system does not treat a red badge as a substitute for an actual approval boundary.

### Synthetic data is a product constraint

The public implementation demonstrates engineering patterns without publishing private content or implying access to production systems. Any future benchmark must use a documented, reproducible dataset.

## Repository structure

```text
ContentOS/
├── app/
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # Pydantic domain and request models
│   ├── orchestrator.py      # Workflow creation and review transitions
│   └── static/              # Dashboard HTML, CSS, and JavaScript
├── docs/
│   ├── architecture.md      # System boundaries and extension points
│   └── workflow.md          # Lifecycle and review model
├── tests/
│   └── test_api.py          # API and state transition tests
├── DESIGN.md                # Interface design direction
├── PRODUCT.md               # Product scope and constraints
├── LICENSE
├── README.md
└── requirements.txt
```

## Current scope and next steps

### Implemented in v0.1

- local FastAPI service;
- deterministic workflow orchestration;
- inspectable task and event state;
- human review actions;
- responsive dashboard;
- automated API tests.

### Planned extensions

- durable persistence with migrations;
- provider adapter interface for real model execution;
- queue-backed parallel workers and retry policies;
- authentication and workspace-level authorization;
- artifact versioning and lineage;
- benchmark fixtures for agreement, latency, and failure recovery;
- richer validation rules and review analytics.

Planned extensions are deliberately listed separately from the current implementation.

## Portfolio note

ContentOS is a public reference implementation inspired by practical AI workflow engineering. It is not presented as a copy of any private deployment, and it makes no production-readiness, accuracy, throughput, or model-performance claims beyond the tests included in this repository.

## License

MIT
