from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class TrafficLevel(str, Enum):
    FREE_FLOW = "FREE_FLOW"
    LIGHT = "LIGHT"
    MODERATE = "MODERATE"
    CONGESTED = "CONGESTED"
    SEVERE = "SEVERE"
    INCIDENT_AFFECTED = "INCIDENT_AFFECTED"
    RECOVERY = "RECOVERY"

class Freshness(str, Enum):
    FRESH = "FRESH"
    AGING = "AGING"
    STALE = "STALE"
    INVALID = "INVALID"

class StateDataQuality(BaseModel):
    overall: float
    camera: float
    tracking: float
    calibration: float
    signal: float
    freshness: float

class LaneTrafficState(BaseModel):
    lane_id: str
    timestamp: datetime
    vehicles: int
    flow_veh_per_hour: float
    average_speed_kmh: float
    density_veh_per_km: float
    queue_length_m: float
    queue_vehicles: int
    occupancy_ratio: float
    delay_seconds: float
    data_quality: float

class ApproachState(BaseModel):
    approach_id: str
    vehicle_count: int
    average_speed_kmh: float
    queue_length_m: float
    flow_veh_per_hour: float
    density_veh_per_km: float
    delay_seconds: float
    lanes: List[LaneTrafficState]

class IntersectionSignalState(BaseModel):
    signal_id: str
    phase: str
    elapsed_seconds: int
    remaining_green_seconds: Optional[int]
    cycle_seconds: Optional[int]
    controller_status: str

class IntersectionState(BaseModel):
    intersection_id: str
    timestamp: datetime
    
    state: TrafficLevel
    congestion_index: float
    
    approaches: Dict[str, ApproachState]
    signal: Optional[IntersectionSignalState] = None
    
    data_quality: StateDataQuality
    
    spillback_risk: float = 0.0

class CorridorState(BaseModel):
    corridor_id: str
    average_speed_kmh: float
    travel_time_seconds: float
    free_flow_seconds: float
    delay_seconds: float
    total_queue_m: float
    bottleneck: Optional[str]
    spillback_risk: float
