from enum import Enum
from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel

class EmergencyState(str, Enum):
    DETECTED = "DETECTED"
    CANDIDATE = "CANDIDATE"
    CORROBORATING = "CORROBORATING"
    VERIFIED = "VERIFIED"
    CLASSIFIED = "CLASSIFIED"
    ACTIVE = "ACTIVE"
    RESPONSE_PLANNING = "RESPONSE_PLANNING"
    RESPONDING = "RESPONDING"
    MITIGATING = "MITIGATING"
    CONTAINED = "CONTAINED"
    RECOVERY = "RECOVERY"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    DISMISSED = "DISMISSED"

class Evidence(BaseModel):
    evidence_id: str
    event_id: str
    evidence_type: str
    source: str
    timestamp: datetime
    location: dict
    confidence: float
    reference: str
    metadata: dict = {}

class EmergencyEvent(BaseModel):
    event_id: str
    tenant_id: str
    event_type: str
    source: str
    source_id: str
    location: dict
    geometry: dict
    detected_at: datetime
    verified_at: Optional[datetime] = None
    severity: str = "UNKNOWN"
    confidence: float
    status: EmergencyState = EmergencyState.CANDIDATE
    affected_assets: List[str] = []
    affected_territory: List[str] = []
    evidence: List[Evidence] = []
    correlation_id: Optional[str] = None
    created_by: str

class ImpactZone(BaseModel):
    event_id: str
    geometry: dict
    radius_or_polygon: str
    affected_roads: List[str]
    affected_intersections: List[str]
    affected_assets: List[str]
    affected_services: List[str]
    confidence: float

class EmergencyResource(BaseModel):
    resource_id: str
    tenant_id: str
    resource_type: str
    organization_id: str
    location: dict
    availability: str
    capability: List[str]
    status: str
    vehicle_id: Optional[str] = None
    crew_id: Optional[str] = None

class EmergencyDecision(BaseModel):
    decision_id: str
    event_id: str
    decision_type: str
    actor: str
    input_state: dict
    recommendation: dict
    approved_action: Optional[dict] = None
    policy_version: str
    safety_version: str
    timestamp: datetime
    outcome: Optional[str] = None
