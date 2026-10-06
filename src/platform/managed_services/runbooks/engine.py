from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class RunbookStatus(str, enum.Enum):
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    MANUAL_INTERVENTION_REQUIRED = "MANUAL_INTERVENTION_REQUIRED"

class RunbookExecution(BaseModel):
    execution_id: str
    runbook_id: str
    target_asset_id: str
    status: RunbookStatus = RunbookStatus.PENDING
    steps_completed: int = 0
    total_steps: int = 1
    logs: List[str] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None

class RunbookEngine:
    def __init__(self):
        self.executions: Dict[str, RunbookExecution] = {}
        
    def trigger_runbook(self, execution: RunbookExecution) -> RunbookExecution:
        self.executions[execution.execution_id] = execution
        return execution
        
    def log_step(self, execution_id: str, log: str, success: bool = True) -> RunbookExecution:
        if execution_id not in self.executions:
            raise ValueError("Execution not found")
            
        exec_record = self.executions[execution_id]
        exec_record.logs.append(log)
        if success:
            exec_record.steps_completed += 1
            if exec_record.steps_completed >= exec_record.total_steps:
                exec_record.status = RunbookStatus.SUCCESS
                exec_record.completed_at = datetime.utcnow()
            else:
                exec_record.status = RunbookStatus.EXECUTING
        else:
            exec_record.status = RunbookStatus.FAILED
            exec_record.completed_at = datetime.utcnow()
            
        return exec_record
