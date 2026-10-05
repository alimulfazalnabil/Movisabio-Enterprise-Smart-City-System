from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class ActivityZone(BaseModel):
    zone_id: str
    activity_types: List[str] # RESIDENTIAL, COMMERCIAL, TOURISM, etc.
    population_estimate: int
    employment_estimate: int
    activity_intensity_profile: Dict[str, float] # hour_of_day -> intensity multiplier

class MobilityDemand(BaseModel):
    origin_zone: str
    destination_zone: str
    time_window_start: datetime
    time_window_end: datetime
    mode: str
    trip_purpose: str
    volume_estimate: int
    confidence: float

class ODMatrix(BaseModel):
    matrix_id: str
    time_window: str # e.g. "08:00-09:00"
    zones: List[str]
    flow_matrix: Dict[str, Dict[str, int]] # origin -> destination -> volume
    timestamp: datetime

class EventDemand(BaseModel):
    event_id: str
    location_zone: str
    start_time: datetime
    end_time: datetime
    expected_attendance: int
    mode_split: Dict[str, float] # mode -> percentage
