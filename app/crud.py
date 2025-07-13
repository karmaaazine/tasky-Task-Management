from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import Task, TaskCreate, TaskUpdate, TaskStatus

class TaskCRUD:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task"""
        task = Task(
            id=self.next_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            created_at=datetime.now(),
            updated_at=None
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        return self.tasks.get(task_id)

    def get_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """Get all tasks, optionally filtered by status"""
        tasks = list(self.tasks.values())
        if status_filter:
            tasks = [task for task in tasks if task.status == status_filter]
        return sorted(tasks, key=lambda x: x.created_at, reverse=True)

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task"""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        task.updated_at = datetime.now()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Get task statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks.values() if task.status == TaskStatus.DONE])
        pending_tasks = len([task for task in self.tasks.values() if task.status == TaskStatus.PENDING])
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
        } 