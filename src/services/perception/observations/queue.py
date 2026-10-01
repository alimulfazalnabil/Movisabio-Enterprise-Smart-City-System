from pydantic import BaseModel
from typing import Optional

class QueueObservation(BaseModel):
    """
    Identifies a queue formed within a single lane.
    """
    lane_id: str
    queue_length_m: float
    queue_vehicle_count: int
    queue_confidence: float

class TravelTimeObservation(BaseModel):
    """
    Captures the time required for a vehicle to traverse a defined segment.
    """
    segment_id: str
    entry_time: float
    exit_time: float
    travel_time_seconds: float
    delay_seconds: float
    reference_free_flow_seconds: float
