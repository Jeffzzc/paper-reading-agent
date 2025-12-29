from fastapi.testclient import TestClient
from app.main import app
from app.services.workflow import workflow_manager
from unittest.mock import MagicMock, AsyncMock

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Should return index.html content
    assert "<!DOCTYPE html>" in response.text

def test_analyze_paper():
    # Mock workflow manager to avoid real processing
    original_create = workflow_manager.create_task
    workflow_manager.create_task = AsyncMock(return_value="test-task-id")
    
    workflow_manager.tasks["test-task-id"] = {
        "task_id": "test-task-id",
        "status": "pending",
        "message": "Task created",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    
    workflow_manager.get_task_status = AsyncMock(return_value={
        "task_id": "test-task-id",
        "status": "pending"
    })

    response = client.post("/api/analyze", json={
        "input_type": "title",
        "value": "Attention is all you need"
    })
    
    assert response.status_code == 200
    assert response.json()["task_id"] == "test-task-id"
    
    # Restore mock
    workflow_manager.create_task = original_create
