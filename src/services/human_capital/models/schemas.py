from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class Skill(BaseModel):
    skill_id: str
    name: str
    category: str

class Occupation(BaseModel):
    occupation_id: str
    title: str
    core_skills: List[str]
    industry: List[str]

class SkillDemand(BaseModel):
    skill_id: str
    territory_id: str
    estimated_demand: float
    period: str # e.g. "2027-Q1"

class SkillSupply(BaseModel):
    skill_id: str
    territory_id: str
    effective_supply: float
    period: str

class SkillGap(BaseModel):
    gap_id: str
    skill_id: str
    territory_id: str
    estimated_demand: float
    effective_supply: float
    gap_value: float
    status: str # HIGH_SHORTAGE, MODERATE_SHORTAGE, BALANCED, SURPLUS

class WorkforceScenario(BaseModel):
    scenario_id: str
    industry: str
    new_jobs: int
    required_skills: Dict[str, float] # skill_id -> percentage of new jobs needing it
