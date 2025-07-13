import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.models import TaskStatus

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Tasky - Task Management API"}

def test_create_task():
    """Test task creation"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Task"
    assert task["description"] == "This is a test task"
    assert task["status"] == "pending"
    assert "id" in task
    assert "created_at" in task
    return task

def test_get_all_tasks():
    """Test getting all tasks"""
    # Create a task first
    test_create_task()
    
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 1

def test_get_task_by_id():
    """Test getting a specific task"""
    # Create a task first
    task = test_create_task()
    task_id = task["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == task["title"]

def test_get_task_not_found():
    """Test getting a non-existent task"""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task():
    """Test updating a task"""
    # Create a task first
    task = test_create_task()
    task_id = task["id"]
    
    update_data = {
        "title": "Updated Task",
        "status": "done"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["status"] == "done"
    assert updated_task["id"] == task_id

def test_update_task_not_found():
    """Test updating a non-existent task"""
    update_data = {"title": "Updated Task"}
    response = client.put("/tasks/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task():
    """Test deleting a task"""
    # Create a task first
    task = test_create_task()
    task_id = task["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
    
    # Verify task is deleted
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_delete_task_not_found():
    """Test deleting a non-existent task"""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_filter_tasks_by_status():
    """Test filtering tasks by status"""
    # Create tasks with different statuses
    pending_task = {
        "title": "Pending Task",
        "description": "This is pending",
        "status": "pending"
    }
    done_task = {
        "title": "Done Task",
        "description": "This is done",
        "status": "done"
    }
    
    client.post("/tasks", json=pending_task)
    client.post("/tasks", json=done_task)
    
    # Test filtering by pending status
    response = client.get("/tasks?status=pending")
    assert response.status_code == 200
    tasks = response.json()
    assert all(task["status"] == "pending" for task in tasks)
    
    # Test filtering by done status
    response = client.get("/tasks?status=done")
    assert response.status_code == 200
    tasks = response.json()
    assert all(task["status"] == "done" for task in tasks)

def test_get_stats():
    """Test getting task statistics"""
    # Clear existing tasks by creating a fresh client
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_tasks" in stats
    assert "completed_tasks" in stats
    assert "pending_tasks" in stats
    assert "completion_rate" in stats

def test_get_metrics():
    """Test getting Prometheus metrics"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    metrics_text = response.text
    assert "http_requests_total" in metrics_text
    assert "http_request_duration_seconds" in metrics_text

def test_task_validation():
    """Test task validation"""
    # Test empty title
    invalid_task = {
        "title": "",
        "description": "Valid description"
    }
    response = client.post("/tasks", json=invalid_task)
    assert response.status_code == 422
    
    # Test title too long
    invalid_task = {
        "title": "x" * 201,  # Exceeds max length
        "description": "Valid description"
    }
    response = client.post("/tasks", json=invalid_task)
    assert response.status_code == 422

def test_task_creation_without_description():
    """Test creating task without description"""
    task_data = {
        "title": "Task without description",
        "status": "pending"
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Task without description"
    assert task["description"] is None
    assert task["status"] == "pending" 