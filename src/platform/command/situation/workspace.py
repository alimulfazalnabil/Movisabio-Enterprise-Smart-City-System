from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import enum

class SituationStatus(str, enum.Enum):
    DETECTED = "DETECTED"
    CANDIDATE = "CANDIDATE"
    ACTIVE = "ACTIVE"
    COORDINATING = "COORDINATING"
    RESPONDING = "RESPONDING"
    MITIGATING = "MITIGATING"
    STABILIZING = "STABILIZING"
    RECOVERY = "RECOVERY"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class SituationWorkspace(BaseModel):
    situation_id: str
    tenant_id: str
    title: str
    severity: str
    status: SituationStatus = SituationStatus.DETECTED
    commander_id: Optional[str] = None
    affected_assets: List[str] = []
    active_tasks: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WorkspaceManager:
    def __init__(self):
        self.workspaces: Dict[str, SituationWorkspace] = {}
        
    def create_workspace(self, workspace: SituationWorkspace) -> SituationWorkspace:
        self.workspaces[workspace.situation_id] = workspace
        return workspace
        
    def escalate_situation(self, situation_id: str, new_severity: str) -> SituationWorkspace:
        if situation_id not in self.workspaces:
            raise ValueError("Workspace not found")
        workspace = self.workspaces[situation_id]
        workspace.severity = new_severity
        workspace.status = SituationStatus.ACTIVE
        return workspace
