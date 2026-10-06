from pydantic import BaseModel
from typing import List, Optional

class Jurisdiction(BaseModel):
    jurisdiction_id: str
    name: str
    type: str # GLOBAL, REGION, COUNTRY, STATE, MUNICIPALITY
    parent_jurisdiction_id: Optional[str] = None
    country_code: str
    status: str = "ACTIVE"

class Requirement(BaseModel):
    requirement_id: str
    jurisdiction_id: str
    source: str
    category: str
    applies_to: List[str]
    controls: List[str]
    status: str = "ACTIVE"

class GovernanceRegistry:
    def __init__(self):
        self.jurisdictions: dict[str, Jurisdiction] = {}
        self.requirements: dict[str, Requirement] = {}
        
    def add_jurisdiction(self, jurisdiction: Jurisdiction) -> None:
        self.jurisdictions[jurisdiction.jurisdiction_id] = jurisdiction
        
    def add_requirement(self, requirement: Requirement) -> None:
        self.requirements[requirement.requirement_id] = requirement
        
    def get_requirements_for_system(self, system: str, jurisdiction_id: str) -> List[Requirement]:
        """Get all active requirements for a system in a jurisdiction."""
        applicable = []
        for req in self.requirements.values():
            if req.jurisdiction_id == jurisdiction_id and system in req.applies_to and req.status == "ACTIVE":
                applicable.append(req)
        return applicable
