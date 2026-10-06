from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class DeveloperStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    VERIFIED = "VERIFIED"
    SUSPENDED = "SUSPENDED"

class Developer(BaseModel):
    developer_id: str
    organization_id: Optional[str] = None
    email: str
    status: DeveloperStatus = DeveloperStatus.REGISTERED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DeveloperRegistry:
    def __init__(self):
        self.developers: Dict[str, Developer] = {}
        
    def register(self, developer: Developer) -> Developer:
        self.developers[developer.developer_id] = developer
        return developer
        
    def verify(self, developer_id: str) -> Developer:
        if developer_id not in self.developers:
            raise ValueError("Developer not found")
        self.developers[developer_id].status = DeveloperStatus.VERIFIED
        return self.developers[developer_id]
