from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import enum

class RequirementStatus(str, enum.Enum):
    CAPTURED = "CAPTURED"
    ANALYZED = "ANALYZED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    IMPLEMENTED = "IMPLEMENTED"
    TESTED = "TESTED"
    ACCEPTED = "ACCEPTED"
    BASELINED = "BASELINED"

class RequirementCategory(str, enum.Enum):
    BUSINESS = "BUSINESS"
    FUNCTIONAL = "FUNCTIONAL"
    TECHNICAL = "TECHNICAL"
    DATA = "DATA"
    SECURITY = "SECURITY"

class ProjectRequirement(BaseModel):
    requirement_id: str
    project_id: str
    title: str
    description: str
    category: RequirementCategory
    status: RequirementStatus = RequirementStatus.CAPTURED
    traceability_links: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RequirementsEngine:
    def __init__(self):
        self.requirements: Dict[str, ProjectRequirement] = {}
        
    def add_requirement(self, req: ProjectRequirement) -> ProjectRequirement:
        self.requirements[req.requirement_id] = req
        return req
        
    def update_status(self, requirement_id: str, new_status: RequirementStatus) -> ProjectRequirement:
        if requirement_id not in self.requirements:
            raise ValueError("Requirement not found")
        self.requirements[requirement_id].status = new_status
        return self.requirements[requirement_id]
