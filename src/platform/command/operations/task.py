from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE = "EN_ROUTE"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class OperationalTask(BaseModel):
    task_id: str
    situation_id: str
    task_type: str
    priority: str
    status: TaskStatus = TaskStatus.PENDING
    assignee_id: Optional[str] = None
    organization_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskEngine:
    def __init__(self):
        self.tasks: Dict[str, OperationalTask] = {}
        
    def create_task(self, task: OperationalTask) -> OperationalTask:
        self.tasks[task.task_id] = task
        return task
        
    def assign_task(self, task_id: str, assignee_id: str) -> OperationalTask:
        if task_id not in self.tasks:
            raise ValueError("Task not found")
        task = self.tasks[task_id]
        task.assignee_id = assignee_id
        task.status = TaskStatus.ASSIGNED
        return task
