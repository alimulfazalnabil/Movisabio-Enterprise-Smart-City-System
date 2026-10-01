from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Point(BaseModel):
    x: float
    y: float

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class VehicleTrack(BaseModel):
    """
    Canonical Track representation bridging Computer Vision to Traffic Intelligence.
    Maintains state across multiple frames.
    """
    track_id: str
    camera_id: str
    vehicle_class: str
    class_confidence: float
    bbox: BoundingBox
    
    first_seen: datetime
    last_seen: datetime
    
    trajectory: List[Point]
    
    current_lane_id: Optional[str] = None
    previous_lane_id: Optional[str] = None
    
    direction: Optional[float] = None
    speed_kmh: Optional[float] = None
    
    detection_confidence: float
    tracking_confidence: float
    status: str  # NEW, ACTIVE, TEMPORARILY_LOST, REIDENTIFIED, EXITED
