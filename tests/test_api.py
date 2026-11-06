from fastapi.testclient import TestClient

from app.main import app, workflows

client = TestClient(app)


def setup_function():
    workflows.clear()


def test_health_is_available():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_workflow_creation_and_review_transition():
    response = client.post("/api/workflows", json={"title": "Feedback loops", "audience": "Engineers", "deliverables": ["slides"]})
    assert response.status_code == 201
    workflow = response.json()
    review_task = next(task for task in workflow["tasks"] if task["state"] == "needs_review")

    reviewed = client.post(f"/api/workflows/{workflow['id']}/tasks/{review_task['id']}/review", json={"decision": "approve", "note": "Aligned to the brief."})
    assert reviewed.status_code == 200
    assert next(task for task in reviewed.json()["tasks"] if task["id"] == review_task["id"])["state"] == "approved"


def test_missing_workflow_is_404():
    assert client.get("/api/workflows/wf_missing").status_code == 404
