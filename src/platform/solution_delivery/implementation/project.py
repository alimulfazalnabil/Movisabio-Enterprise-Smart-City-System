from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class ImplementationPhase(str, enum.Enum):
    DISCOVERY = "DISCOVERY"
    DESIGN = "DESIGN"
    IMPLEMENTATION = "IMPLEMENTATION"
    TESTING = "TESTING"
    PILOT = "PILOT"
    COMMISSIONING = "COMMISSIONING"
    HANDOVER = "HANDOVER"

class DeliveryProject(BaseModel):
    project_id: str
    customer_id: str
    name: str
    phase: ImplementationPhase = ImplementationPhase.DISCOVERY
    tasks: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DeliveryEngine:
    def __init__(self):
        self.projects: Dict[str, DeliveryProject] = {}
        
    def create_project(self, project: DeliveryProject) -> DeliveryProject:
        self.projects[project.project_id] = project
        return project
        
    def advance_phase(self, project_id: str, new_phase: ImplementationPhase) -> DeliveryProject:
        if project_id not in self.projects:
            raise ValueError("Project not found")
        self.projects[project_id].phase = new_phase
        return self.projects[project_id]
