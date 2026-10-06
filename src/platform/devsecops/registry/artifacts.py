from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class Artifact(BaseModel):
    artifact_id: str
    digest: str
    version: str
    commit_sha: str
    sbom_uri: str
    signature: Optional[str] = None
    created_at: datetime
    approved_for_prod: bool = False

class ArtifactRegistry:
    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}
        
    def register(self, artifact: Artifact) -> None:
        self.artifacts[artifact.artifact_id] = artifact
        
    def approve(self, artifact_id: str) -> bool:
        if artifact_id in self.artifacts:
            self.artifacts[artifact_id].approved_for_prod = True
            return True
        return False
        
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        return self.artifacts.get(artifact_id)
