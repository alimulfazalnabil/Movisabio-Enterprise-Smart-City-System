from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SpeedEstimate(BaseModel):
    value: float
    unit: str = "km/h"
    confidence: float

class VehicleDetection(BaseModel):
    confidence: float

class VehicleObservation(BaseModel):
    observation_id: str
    track_id: str
    vehicle_type: str # car, truck, bus, motorcycle
    
    camera_id: str
    intersection_id: Optional[str]
    lane_id: Optional[str]
    
    timestamp: datetime
    
    position: dict # e.g. {"x": 423, "y": 211}
    speed: Optional[SpeedEstimate] = None
    detection: VehicleDetection

class LaneState(BaseModel):
    lane_id: str
    vehicle_count: int
    average_speed_kmh: float
    queue_length: int # in meters or vehicles
    occupancy: float  # 0.0 to 1.0
    flow_rate: float
    density: float
    confidence: float

class IntersectionMetrics(BaseModel):
    vehicle_count: int
    average_speed_kmh: float
    density: float
    queue_length: int
    congestion_index: float

class SignalState(BaseModel):
    phase: str
    remaining_seconds: int

class TrafficDataQuality(BaseModel):
    score: float

class IntersectionTrafficState(BaseModel):
    """
    Canonical output of the Data Ingestion & Computer Vision Pipeline.
    Consumed by RL Optimization, Digital Twin, and Analytics.
    """
    intersection_id: str
    timestamp: datetime
    
    traffic: IntersectionMetrics
    
    lanes: List[LaneState] = Field(default_factory=list)
    
    signal: Optional[SignalState] = None
    
    data_quality: TrafficDataQuality
