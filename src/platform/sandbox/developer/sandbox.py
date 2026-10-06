from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class SandboxEnvironment(BaseModel):
    sandbox_id: str
    developer_id: str
    application_id: str
    synthetic_tenant_id: str
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SandboxManager:
    def __init__(self):
        self.sandboxes: Dict[str, SandboxEnvironment] = {}
        
    def provision_sandbox(self, sandbox: SandboxEnvironment) -> SandboxEnvironment:
        self.sandboxes[sandbox.sandbox_id] = sandbox
        return sandbox
