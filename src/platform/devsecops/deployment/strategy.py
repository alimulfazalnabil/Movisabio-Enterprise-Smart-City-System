from typing import List, Dict, Optional
from datetime import datetime
from src.platform.devsecops.registry.artifacts import Artifact

class Deployment:
    def __init__(self, deployment_id: str, artifact: Artifact, environment: str):
        self.deployment_id = deployment_id
        self.artifact = artifact
        self.environment = environment
        self.status = "PENDING"
        self.rollout_percentage = 0
        self.started_at = datetime.now()
        
    def progress_rollout(self, percentage: int) -> bool:
        if not self.artifact.approved_for_prod and self.environment == "PRODUCTION":
            self.status = "BLOCKED_UNAPPROVED"
            return False
            
        self.rollout_percentage = percentage
        if self.rollout_percentage >= 100:
            self.status = "COMPLETED"
        else:
            self.status = "IN_PROGRESS"
        return True
        
    def rollback(self) -> None:
        self.status = "ROLLED_BACK"
        self.rollout_percentage = 0

class DeploymentController:
    def __init__(self):
        self.deployments: List[Deployment] = []
        
    def create_deployment(self, artifact: Artifact, environment: str) -> Deployment:
        deployment = Deployment(f"deploy-{len(self.deployments) + 1}", artifact, environment)
        self.deployments.append(deployment)
        return deployment
