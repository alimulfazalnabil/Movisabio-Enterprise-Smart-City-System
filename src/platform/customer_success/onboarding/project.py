from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class MilestoneStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"

class OnboardingMilestone(BaseModel):
    milestone_id: str
    name: str
    status: MilestoneStatus = MilestoneStatus.PENDING
    dependencies: List[str] = Field(default_factory=list)

class OnboardingProject(BaseModel):
    project_id: str
    customer_id: str
    tenant_id: str
    milestones: Dict[str, OnboardingMilestone] = Field(default_factory=dict)
    is_live: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OnboardingManager:
    def __init__(self):
        self.projects: Dict[str, OnboardingProject] = {}
        
    def create_project(self, project: OnboardingProject) -> OnboardingProject:
        self.projects[project.project_id] = project
        return project
        
    def complete_milestone(self, project_id: str, milestone_id: str) -> bool:
        if project_id not in self.projects:
            return False
            
        project = self.projects[project_id]
        if milestone_id in project.milestones:
            project.milestones[milestone_id].status = MilestoneStatus.COMPLETED
            
            # Check if all completed
            if all(m.status == MilestoneStatus.COMPLETED for m in project.milestones.values()):
                project.is_live = True
            return True
        return False
