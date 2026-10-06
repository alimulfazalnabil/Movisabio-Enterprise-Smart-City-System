from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class SkillRequirement(BaseModel):
    skill_name: str
    required_count: int
    available_count: int
    
    @property
    def gap(self) -> int:
        return max(0, self.required_count - self.available_count)

class AllocationEngine:
    def __init__(self):
        self.requirements: Dict[str, SkillRequirement] = {}
        
    def add_requirement(self, req: SkillRequirement) -> SkillRequirement:
        self.requirements[req.skill_name] = req
        return req
        
    def analyze_gaps(self) -> Dict[str, int]:
        gaps = {}
        for skill, req in self.requirements.items():
            if req.gap > 0:
                gaps[skill] = req.gap
        return gaps
        
    def recommend_action(self, skill: str) -> str:
        if skill not in self.requirements or self.requirements[skill].gap == 0:
            return "NO_ACTION_REQUIRED"
            
        gap = self.requirements[skill].gap
        if gap > 10:
            return "STRATEGIC_PARTNERSHIP_OR_AGENCY"
        elif gap > 3:
            return "ACCELERATE_HIRING"
        else:
            return "INTERNAL_TRAINING_OR_CONTRACTOR"
