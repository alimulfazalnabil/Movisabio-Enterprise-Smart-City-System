from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class AppStatus(str, enum.Enum):
    DEVELOPMENT = "DEVELOPMENT"
    SANDBOX = "SANDBOX"
    REVIEW = "REVIEW"
    PRODUCTION = "PRODUCTION"
    SUSPENDED = "SUSPENDED"
    DEPRECATED = "DEPRECATED"

class DeveloperApplication(BaseModel):
    application_id: str
    developer_id: str
    name: str
    status: AppStatus = AppStatus.DEVELOPMENT
    allowed_scopes: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ApplicationRegistry:
    def __init__(self):
        self.applications: Dict[str, DeveloperApplication] = {}
        
    def register_app(self, app: DeveloperApplication) -> DeveloperApplication:
        self.applications[app.application_id] = app
        return app
        
    def update_status(self, application_id: str, new_status: AppStatus) -> DeveloperApplication:
        if application_id not in self.applications:
            raise ValueError("Application not found")
        self.applications[application_id].status = new_status
        return self.applications[application_id]
