from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime, timezone

class Widget(BaseModel):
    widget_id: str
    type: str
    configuration: Dict[str, Any]

class Workspace(BaseModel):
    workspace_id: str
    user_id: str
    tenant_id: str
    name: str
    role_target: str
    widgets: List[Widget]
    created_at: datetime

class WorkspaceManager:
    def __init__(self):
        self.workspaces: Dict[str, Workspace] = {}
        
    def create_workspace(self, workspace: Workspace) -> None:
        self.workspaces[workspace.workspace_id] = workspace
        
    def get_user_workspaces(self, user_id: str, tenant_id: str) -> List[Workspace]:
        return [w for w in self.workspaces.values() if w.user_id == user_id and w.tenant_id == tenant_id]
