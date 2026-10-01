from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PriorityClass(str, Enum):
    P0_CRITICAL_EMERGENCY = "P0"
    P1_EMERGENCY_SERVICE = "P1"  # Ambulance / Fire / Police
    P2_PUBLIC_TRANSIT = "P2"
    P3_TRANSIT_DELAY_RECOVERY = "P3"
    P4_GENERAL_OPTIMIZATION = "P4"
    P5_BACKGROUND_OPTIMIZATION = "P5"

class PriorityStatus(str, Enum):
    REQUESTED = "REQUESTED"
    AUTHORIZED = "AUTHORIZED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    GRANTED = "GRANTED"
    PREEMPTED = "PREEMPTED"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"

class PriorityRequest(BaseModel):
    request_id: str
    tenant_id: str
    vehicle_id: str
    vehicle_type: str
    priority_class: PriorityClass
    route_id: Optional[str]
    current_position: Optional[dict]
    heading: Optional[float]
    speed: Optional[float]
    
    target_intersection_id: str
    target_lane_id: Optional[str]
    estimated_arrival_time: datetime
    requested_phase: str
    
    urgency: int  # 1 to 10
    reason: str
    source: str   # 'GPS', 'CCTV', 'V2X'
    confidence: float
    
    status: PriorityStatus = PriorityStatus.REQUESTED
    created_at: datetime
    expires_at: datetime
