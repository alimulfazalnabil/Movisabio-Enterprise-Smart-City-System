from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import enum

class DeploymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    SCANNING = "SCANNING"
    STAGING = "STAGING"
    DEPLOYING = "DEPLOYING"
    ACTIVE = "ACTIVE"
    ROLLED_BACK = "ROLLED_BACK"

class ApplicationDeployment(BaseModel):
    deployment_id: str
    application_id: str
    version: str
    status: DeploymentStatus = DeploymentStatus.PENDING
    sbom_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DeploymentEngine:
    def __init__(self):
        self.deployments: Dict[str, ApplicationDeployment] = {}
        
    def start_deployment(self, deployment: ApplicationDeployment) -> ApplicationDeployment:
        self.deployments[deployment.deployment_id] = deployment
        return deployment
        
    def advance_deployment(self, deployment_id: str, status: DeploymentStatus) -> ApplicationDeployment:
        if deployment_id not in self.deployments:
            raise ValueError("Deployment not found")
        self.deployments[deployment_id].status = status
        return self.deployments[deployment_id]
