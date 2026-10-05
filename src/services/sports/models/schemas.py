from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class SportsAsset(BaseModel):
    asset_id: str
    territory_id: str
    asset_type: str # STADIUM, SPORTS_COMPLEX, GYMNASIUM, etc.
    name: str
    nominal_capacity: int
    operational_status: str

class FacilityCapacity(BaseModel):
    facility_id: str
    nominal_capacity: int
    scheduled_capacity: int
    current_occupancy: int
    occupancy_confidence: float

class RecreationDemand(BaseModel):
    territory_id: str
    population: int
    active_population_ratio: float

class RecreationAccessibility(BaseModel):
    territory_id: str
    accessible_capacity: int
    service_gap: int
    status: str # LOW_GAP, MODERATE_GAP, HIGH_GAP, CRITICAL_GAP

class SportsEvent(BaseModel):
    event_id: str
    venue_id: str
    expected_attendance: int
    status: str # PLANNED, APPROVED, ACTIVE
