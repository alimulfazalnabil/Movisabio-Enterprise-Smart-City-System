from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class TourismDestination(BaseModel):
    destination_id: str
    category: str # ATTRACTION, BEACH, PARK, HERITAGE_SITE, EVENT_VENUE
    location: str
    capacity: int
    status: str

class AttractionCapacity(BaseModel):
    attraction_id: str
    safe_capacity: int
    current_visitors: int
    entry_rate: float
    exit_rate: float

class VisitorDemandForecast(BaseModel):
    destination_zone: str
    target_time: datetime
    expected_visitors: int
    confidence_interval: float

class TourismEvent(BaseModel):
    event_id: str
    venue_id: str
    expected_attendance: int
    impact_level: str # LOW, MODERATE, HIGH, CRITICAL
