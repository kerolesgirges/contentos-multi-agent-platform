from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskState(str, Enum):
    queued = "queued"
    running = "running"
    needs_review = "needs_review"
    approved = "approved"
    failed = "failed"


class WorkflowRequest(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    audience: str = Field(min_length=3, max_length=120)
    deliverables: list[str] = Field(min_length=1)


class ReviewRequest(BaseModel):
    decision: str = Field(pattern="^(approve|revise)$")
    note: str = Field(default="", max_length=500)


class Event(BaseModel):
    timestamp: datetime
    label: str
    detail: str


class Task(BaseModel):
    id: str
    name: str
    kind: str
    state: TaskState
    owner: str
    duration_ms: int | None = None
    artifact_id: str | None = None
    summary: str
    confidence: int | None = None
    review_note: str | None = None


class Workflow(BaseModel):
    id: str
    title: str
    audience: str
    state: TaskState
    created_at: datetime
    tasks: list[Task]
    events: list[Event]
