from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class RoadSegment(BaseModel):
    segment_id: str
    source_intersection_id: str
    target_intersection_id: str
    length_meters: float
    capacity_vph: int
    current_flow: int
    current_speed: float
    queue_length_meters: float
    timestamp: datetime

class Corridor(BaseModel):
    corridor_id: str
    intersections: List[str] # Ordered sequence
    segments: List[str]      # Ordered sequence

class SpillbackEvent(BaseModel):
    event_id: str
    segment_id: str
    spillback_probability: float
    affected_upstream_intersection: str
    estimated_time_to_spillback_sec: float
    timestamp: datetime

class SignalPlanCandidate(BaseModel):
    plan_id: str
    corridor_id: str
    cycle_length_sec: int
    offsets: Dict[str, int] # intersection_id -> offset
    objective_weights: Dict[str, float]
    predicted_delay_reduction: float
