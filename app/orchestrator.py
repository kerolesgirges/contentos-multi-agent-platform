from datetime import datetime, timezone
from uuid import uuid4

from .models import Event, Task, TaskState, Workflow, WorkflowRequest


def now() -> datetime:
    return datetime.now(timezone.utc)


def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


def create_workflow(request: WorkflowRequest) -> Workflow:
    workflow_id = make_id("wf")
    tasks: list[Task] = [
        Task(id=make_id("tsk"), name="Shape requirements", kind="planning", state=TaskState.approved, owner="Planner", duration_ms=1840, artifact_id=make_id("art"), summary=f"Clarified outcomes for {request.audience}.", confidence=96),
        Task(id=make_id("tsk"), name="Draft slide outline", kind="slides", state=TaskState.needs_review if "slides" in request.deliverables else TaskState.approved, owner="Slide worker", duration_ms=4210, artifact_id=make_id("art"), summary="12-slide outline with pacing notes and learning objectives.", confidence=88),
        Task(id=make_id("tsk"), name="Write reading material", kind="reading_material", state=TaskState.running if "reading_material" in request.deliverables else TaskState.approved, owner="Docs worker", duration_ms=None, artifact_id=make_id("art"), summary="Structured draft with examples and a glossary.", confidence=None),
        Task(id=make_id("tsk"), name="Build knowledge check", kind="quiz", state=TaskState.queued if "quiz" in request.deliverables else TaskState.approved, owner="Assessment worker", duration_ms=None, artifact_id=make_id("art"), summary="Scenario-based questions aligned to the stated outcomes.", confidence=None),
        Task(id=make_id("tsk"), name="Validate artifact set", kind="validation", state=TaskState.queued, owner="QA worker", duration_ms=None, artifact_id=None, summary="Cross-check objectives, terminology, and deliverable consistency.", confidence=None),
    ]
    events = [
        Event(timestamp=now(), label="Workflow created", detail="Brief accepted and dependency graph assembled."),
        Event(timestamp=now(), label="Planner completed", detail="Requirements artifact approved automatically."),
        Event(timestamp=now(), label="Review checkpoint opened", detail="Slide outline is waiting for a human decision."),
    ]
    return Workflow(id=workflow_id, title=request.title, audience=request.audience, state=TaskState.needs_review, created_at=now(), tasks=tasks, events=events)


def apply_review(workflow: Workflow, task_id: str, decision: str, note: str) -> Workflow:
    task = next((item for item in workflow.tasks if item.id == task_id), None)
    if task is None:
        raise KeyError(task_id)
    if task.state != TaskState.needs_review:
        raise ValueError("Only tasks in needs_review can receive a review decision")
    task.state = TaskState.approved if decision == "approve" else TaskState.running
    task.review_note = note or None
    workflow.events.insert(0, Event(timestamp=now(), label=f"Review: {decision}", detail=note or "Decision recorded by reviewer."))
    workflow.state = TaskState.needs_review if any(t.state == TaskState.needs_review for t in workflow.tasks) else TaskState.running
    return workflow
