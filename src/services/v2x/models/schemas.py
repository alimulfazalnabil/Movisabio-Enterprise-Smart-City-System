from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class TrustState(str, Enum):
    TRUSTED = "TRUSTED"
    CONDITIONALLY_TRUSTED = "CONDITIONALLY_TRUSTED"
    UNVERIFIED = "UNVERIFIED"
    SUSPICIOUS = "SUSPICIOUS"
    REJECTED = "REJECTED"

class V2XMessage(BaseModel):
    message_id: str
    message_type: str
    version: str
    asset_id: str
    timestamp: datetime
    position: Dict[str, float]
    speed_mps: float
    heading_deg: float
    acceleration_mps2: Optional[float] = None
    source: str
    quality: str
    signature: str

class CooperativeObject(BaseModel):
    object_id: str
    object_type: str # VEHICLE, PEDESTRIAN, etc.
    position: Dict[str, float]
    velocity_mps: float
    heading_deg: float
    sources: List[str]
    confidence: float
    state: str # MOVING, STOPPED
    last_updated: datetime

class CollisionRiskCandidate(BaseModel):
    risk_id: str
    object_a_id: str
    object_b_id: str
    time_to_collision_sec: float
    conflict_point: Dict[str, float]
    confidence: float
    timestamp: datetime
