# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: FastAPI backend with a dependency-light static frontend so the reference implementation runs locally without API keys or a frontend build step.

## Users

AI engineers, hiring managers, and technical reviewers evaluating how the author designs reliable AI-assisted workflows.

## Product Purpose

ContentOS is a public reference implementation for coordinating AI workers, artifacts, task state, and human approvals across a multi-stage content workflow. Success means a reviewer can run the demo, inspect the workflow, understand what happened, and see where human judgment enters the system.

## Positioning

The project treats AI generation as one step inside a traceable workflow rather than as a single opaque prompt. Its differentiator is explicit task state, artifact lineage, review checkpoints, and replaceable model adapters.

## Operating Context

The demo uses fictional requests and synthetic content artifacts. A user submits a brief, the orchestrator creates dependent tasks, workers produce structured artifacts, validation records findings, and a reviewer approves or requests revision.

## Capabilities and Constraints

- Implement a local demo with no API key required.
- Expose workflow and task state through a FastAPI API.
- Include deterministic mock workers for planning, slide, reading-material, quiz, and review tasks.
- Include a browser dashboard for inspecting tasks, artifacts, events, and review actions.
- Keep private company names, private data, credentials, and unverifiable production claims out of the repository.
- Clearly label synthetic data and distinguish implemented behavior from planned extensions.

## Brand Commitments

The voice is practical, technical, curious, product-minded, and honest about evidence. The project should feel like an engineer showing their system thinking, not a generic AI marketing site.

## Evidence on Hand

The attached conversation describes prior experience with AI-assisted content workflows and the intended public architecture. No proprietary source code or production deployment evidence is available in this workspace, so the public implementation must stand on its own.

## Product Principles

- Make workflow state visible.
- Prefer structured intermediate artifacts over opaque generation.
- Keep model inference replaceable.
- Make failures recoverable and review decisions explicit.
- Demonstrate behavior with synthetic data instead of unsupported claims.

## Accessibility & Inclusion

Use semantic HTML, keyboard-visible focus, readable contrast, responsive layouts, and status text that is not conveyed by color alone.
