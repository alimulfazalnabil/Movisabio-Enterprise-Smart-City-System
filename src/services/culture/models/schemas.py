from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class CulturalAsset(BaseModel):
    asset_id: str
    territory_id: str
    name: str
    asset_type: str # HERITAGE_SITE, MUSEUM, etc.
    status: str
    data_quality: str

class HeritageRiskIndicator(BaseModel):
    asset_id: str
    hazard: float
    exposure: float
    vulnerability: float
    risk_score: float

class CulturalEvent(BaseModel):
    event_id: str
    name: str
    expected_capacity: int
    status: str # PLANNED, APPROVED, ACTIVE

class EventImpactSimulation(BaseModel):
    event_id: str
    transit_demand: float
    waste_demand: float
    energy_demand: float
