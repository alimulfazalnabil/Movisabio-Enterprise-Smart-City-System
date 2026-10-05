from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ZoneOccupancy(BaseModel):
    zone_id: str
    estimated_occupancy: int
    max_capacity: int
    comfort_score: float

class BuildingEnergy(BaseModel):
    building_id: str
    current_kw: float
    baseline_kw: float
    dr_active: bool # Demand Response Active

class BuildingSafetyEvent(BaseModel):
    event_id: str
    building_id: str
    event_type: str # FIRE, SECURITY, HVAC_FAIL
    severity: str
    timestamp: datetime
