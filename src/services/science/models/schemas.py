from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class Researcher(BaseModel):
    researcher_id: str
    institution_id: str
    expertise: List[str]

class Publication(BaseModel):
    publication_id: str
    title: str
    authors: List[str]
    citations: List[str] # List of publication IDs
    evidence_level: str # PRIMARY_RESEARCH, SYSTEMATIC_REVIEW, AI_GENERATED_HYPOTHESIS

class Experiment(BaseModel):
    experiment_id: str
    project_id: str
    code_version: str
    dataset_version: str
    parameters: Dict[str, str]
    status: str # DESIGN, RUNNING, COMPLETED, FAILED

class Technology(BaseModel):
    technology_id: str
    name: str
    trl: int # Technology Readiness Level (1-9)
    ip_status: str
