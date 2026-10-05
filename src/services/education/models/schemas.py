from typing import List, Dict, Optional
from pydantic import BaseModel

class EducationInstitution(BaseModel):
    institution_id: str
    institution_type: str # SCHOOL, COLLEGE, UNIVERSITY, TRAINING_CENTER, RESEARCH_INSTITUTE
    location: str
    capacity: int
    status: str

class CampusOccupancy(BaseModel):
    campus_id: str
    current_occupancy: int
    peak_capacity: int

class SkillGap(BaseModel):
    skill_name: str
    industry_demand: int
    training_capacity: int
    gap_status: str # SURPLUS, BALANCED, SHORTAGE

class InternshipMatch(BaseModel):
    student_id: str
    company_id: str
    skill_match_score: float
    distance_km: float
