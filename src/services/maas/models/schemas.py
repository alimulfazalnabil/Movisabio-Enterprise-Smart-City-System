from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class JourneyLeg(BaseModel):
    mode: str
    origin: str
    destination: str
    start_time: datetime
    end_time: datetime
    travel_time_sec: int
    cost: float
    provider_id: str
    emissions_estimate: float
    distance_meters: float

class JourneyPlan(BaseModel):
    plan_id: str
    origin: str
    destination: str
    legs: List[JourneyLeg]
    total_travel_time_sec: int
    total_cost: float
    total_emissions: float
    transfers: int
    score: float # Contextual score based on user objective

class DisruptionEvent(BaseModel):
    event_id: str
    provider_id: str
    affected_services: List[str]
    severity: str
    description: str
    timestamp: datetime
