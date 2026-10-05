from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class WorkflowInstance(BaseModel):
    workflow_instance_id: str
    workflow_id: str
    workflow_version: str
    tenant_id: str
    correlation_id: str
    status: str # CREATED, RUNNING, WAITING, APPROVAL_REQUIRED, AUTHORIZED, EXECUTING, COMPLETED, FAILED, COMPENSATING
    context: Dict[str, Any]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class WorkflowStep(BaseModel):
    step_id: str
    workflow_instance_id: str
    step_type: str
    status: str
    attempt_count: int = 0
