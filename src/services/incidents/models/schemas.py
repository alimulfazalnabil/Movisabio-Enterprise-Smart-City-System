from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class IncidentType(str, Enum):
    VEHICLE_STOPPED = "VEHICLE_STOPPED"
    ABNORMAL_SLOWDOWN = "ABNORMAL_SLOWDOWN"
    QUEUE_SPIKE = "QUEUE_SPIKE"
    QUEUE_SPILLOVER = "QUEUE_SPILLOVER"
    LANE_BLOCKAGE = "LANE_BLOCKAGE"
    WRONG_WAY_CANDIDATE = "WRONG_WAY_CANDIDATE"
    COLLISION_CANDIDATE = "COLLISION_CANDIDATE"
    HAZARD_CANDIDATE = "HAZARD_CANDIDATE"

class IncidentSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    CANDIDATE = "CANDIDATE"
    CORROBORATING = "CORROBORATING"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    MITIGATING = "MITIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    DISMISSED = "DISMISSED"

class GeoPoint(BaseModel):
    lat: float
    lon: float

class EvidenceRef(BaseModel):
    evidence_id: str
    type: str # 'TRAJECTORY', 'TRAFFIC_STATE', 'CCTV'
    source: str
    timestamp: datetime
    confidence: float
    
class Incident(BaseModel):
    incident_id: str
    tenant_id: str
    city_id: str
    site_id: str
    intersection_id: Optional[str] = None
    
    incident_type: IncidentType
    status: IncidentStatus
    severity: IncidentSeverity
    confidence: float
    
    detected_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    
    location: Optional[GeoPoint] = None
    source_ids: List[str]
    evidence: List[EvidenceRef]
    affected_lanes: List[str]
    affected_signal_groups: List[str]
    description: str
