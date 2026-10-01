from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class VehicleMobilityState(str, Enum):
    MOVING = "MOVING"
    SLOW = "SLOW"
    STOPPED = "STOPPED"
    ACCELERATING = "ACCELERATING"
    DECELERATING = "DECELERATING"
    LOST = "LOST"
    EXITED = "EXITED"

class StopReason(str, Enum):
    SIGNAL_STOP = "SIGNAL_STOP"
    QUEUE_STOP = "QUEUE_STOP"
    INCIDENT_STOP = "INCIDENT_STOP"
    PARKED = "PARKED"
    UNKNOWN_STOP = "UNKNOWN_STOP"

class TrajectoryPoint(BaseModel):
    timestamp: datetime
    image_x: float
    image_y: float
    world_x: float
    world_y: float
    lane_id: Optional[str] = None
    confidence: float

class TrajectoryQuality(BaseModel):
    tracking: float
    calibration: float
    trajectory: float
    timestamp: float

class SpeedObservation(BaseModel):
    speed_kmh: float
    acceleration_ms2: float
    state: VehicleMobilityState
    confidence: float
    quality: TrajectoryQuality
