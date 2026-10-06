from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class RuntimeStatus(str, enum.Enum):
    PROVISIONING = "PROVISIONING"
    STARTING = "STARTING"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    SUSPENDED = "SUSPENDED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"

class ApplicationRuntime(BaseModel):
    runtime_id: str
    application_id: str
    instance_id: str
    tenant_id: str
    status: RuntimeStatus = RuntimeStatus.PROVISIONING
    resources: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RuntimeEngine:
    def __init__(self):
        self.runtimes: Dict[str, ApplicationRuntime] = {}
        
    def provision_runtime(self, runtime: ApplicationRuntime) -> ApplicationRuntime:
        self.runtimes[runtime.runtime_id] = runtime
        return runtime
        
    def update_status(self, runtime_id: str, new_status: RuntimeStatus) -> ApplicationRuntime:
        if runtime_id not in self.runtimes:
            raise ValueError("Runtime not found")
        self.runtimes[runtime_id].status = new_status
        return self.runtimes[runtime_id]
