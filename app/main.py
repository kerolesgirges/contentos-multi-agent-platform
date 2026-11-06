from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import ReviewRequest, WorkflowRequest
from .orchestrator import apply_review, create_workflow

app = FastAPI(title="ContentOS API", version="0.1.0", description="Reference workflow orchestration API")
workflows = {}
static_dir = Path(__file__).parent / "static"
app.mount("/assets", StaticFiles(directory=static_dir), name="assets")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(static_dir / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "contentos", "mode": "synthetic-demo"}


@app.get("/api/workflows")
def list_workflows():
    return list(workflows.values())


@app.post("/api/workflows", status_code=201)
def new_workflow(request: WorkflowRequest):
    workflow = create_workflow(request)
    workflows[workflow.id] = workflow
    return workflow


@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    workflow = workflows.get(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@app.post("/api/workflows/{workflow_id}/tasks/{task_id}/review")
def review_task(workflow_id: str, task_id: str, request: ReviewRequest):
    workflow = workflows.get(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    try:
        return apply_review(workflow, task_id, request.decision, request.note)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
