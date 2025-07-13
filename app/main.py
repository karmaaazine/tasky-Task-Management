from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from .models import Task, TaskCreate, TaskUpdate
from .crud import TaskCRUD
from .metrics import registry, REQUEST_COUNT, REQUEST_TIME, update_task_metrics
from prometheus_client import generate_latest
from fastapi.responses import Response
import time

app = FastAPI(title="Tasky - Task Management API", version="1.0.0")
task_crud = TaskCRUD()

# Middleware for metrics
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    REQUEST_TIME.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to Tasky - Task Management API"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks(status: Optional[str] = None):
    """Get all tasks, optionally filtered by status"""
    return task_crud.get_tasks(status_filter=status)

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    """Create a new task"""
    return task_crud.create_task(task)

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = task_crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task"""
    task = task_crud.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    success = task_crud.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@app.get("/metrics")
async def get_metrics():
    """Return Prometheus metrics"""
    update_task_metrics(task_crud)
    return Response(generate_latest(registry), media_type="text/plain")

@app.get("/stats")
async def get_stats():
    """Get task statistics"""
    return task_crud.get_stats() 