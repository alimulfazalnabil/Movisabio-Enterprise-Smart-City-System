from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import enum

class IncidentSeverity(str, enum.Enum):
    P1 = "P1" # Critical
    P2 = "P2" # Major
    P3 = "P3" # Moderate
    P4 = "P4" # Minor

class IncidentStatus(str, enum.Enum):
    DETECTED = "DETECTED"
    TRIAGE = "TRIAGE"
    RESPONDING = "RESPONDING"
    REMEDIATED = "REMEDIATED"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"

class OperationsIncident(BaseModel):
    incident_id: str
    tenant_id: str
    service_id: str
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.DETECTED
    description: str
    root_cause: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

class IncidentEngine:
    def __init__(self):
        self.incidents: Dict[str, OperationsIncident] = {}
        
    def create_incident(self, incident: OperationsIncident) -> OperationsIncident:
        self.incidents[incident.incident_id] = incident
        return incident
        
    def update_status(self, incident_id: str, status: IncidentStatus, root_cause: Optional[str] = None) -> OperationsIncident:
        if incident_id not in self.incidents:
            raise ValueError("Incident not found")
        
        inc = self.incidents[incident_id]
        inc.status = status
        if root_cause:
            inc.root_cause = root_cause
            
        if status == IncidentStatus.CLOSED:
            inc.resolved_at = datetime.utcnow()
            
        return inc
