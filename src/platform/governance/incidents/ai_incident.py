from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class AIIncidentSeverity(str, enum.Enum):
    AI_P0 = "AI-P0" # Critical safety
    AI_P1 = "AI-P1" # Major operational
    AI_P2 = "AI-P2" # Significant business
    AI_P3 = "AI-P3" # Limited
    AI_P4 = "AI-P4" # Informational

class AIIncidentStatus(str, enum.Enum):
    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    REMEDIATED = "REMEDIATED"
    CLOSED = "CLOSED"

class AIIncident(BaseModel):
    incident_id: str
    decision_id: str
    severity: AIIncidentSeverity
    description: str
    status: AIIncidentStatus = AIIncidentStatus.DETECTED
    root_cause: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIIncidentManager:
    def __init__(self):
        self.incidents: Dict[str, AIIncident] = {}
        
    def report_incident(self, incident: AIIncident) -> AIIncident:
        self.incidents[incident.incident_id] = incident
        return incident
        
    def resolve_incident(self, incident_id: str, root_cause: str) -> AIIncident:
        if incident_id not in self.incidents:
            raise ValueError("Incident not found")
            
        incident = self.incidents[incident_id]
        incident.root_cause = root_cause
        incident.status = AIIncidentStatus.REMEDIATED
        return incident
