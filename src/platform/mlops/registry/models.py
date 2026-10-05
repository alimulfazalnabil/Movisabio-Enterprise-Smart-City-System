from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class MLModelVersion(BaseModel):
    version_id: str
    model_id: str
    version: str
    dataset_version_id: Optional[str] = None
    feature_version: Optional[str] = None
    artifact_uri: str
    signature: Optional[str] = None
    status: str # REGISTERED, TRAINED, EVALUATED, APPROVED, SHADOW, CANARY, PRODUCTION, DEPRECATED
    created_at: datetime

class MLModel(BaseModel):
    model_id: str
    name: str
    domain: str
    model_type: str
    risk_class: str # R0, R1, R2, R3, R4, R5
    versions: Dict[str, MLModelVersion] = Field(default_factory=dict)
    
    def add_version(self, version: MLModelVersion):
        self.versions[version.version_id] = version
        
    def get_version(self, version_id: str) -> Optional[MLModelVersion]:
        return self.versions.get(version_id)
