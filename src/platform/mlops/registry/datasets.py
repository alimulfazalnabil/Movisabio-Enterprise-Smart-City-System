from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DatasetVersion(BaseModel):
    version_id: str
    dataset_id: str
    version: str
    status: str # REGISTERED, VALIDATING, CURATED, APPROVED, ACTIVE, ARCHIVED
    quality_score: float
    created_at: datetime

class Dataset(BaseModel):
    dataset_id: str
    name: str
    owner: str
    classification: str
    purpose: str
