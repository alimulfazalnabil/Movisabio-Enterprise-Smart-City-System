from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Incident(BaseModel):
    incident_id: str
    severity: str # P0, P1, P2, P3, P4
    service_id: str
    status: str # DETECTED, TRIAGED, INVESTIGATING, MITIGATING, RECOVERING, RESOLVED
    detected_at: datetime
    resolved_at: Optional[datetime] = None

class IncidentCommand:
    def __init__(self):
        self.incidents: List[Incident] = []
        
    def declare_incident(self, service_id: str, severity: str, timestamp: datetime) -> Incident:
        incident = Incident(
            incident_id=f"inc-{len(self.incidents) + 1}",
            severity=severity,
            service_id=service_id,
            status="DETECTED",
            detected_at=timestamp
        )
        self.incidents.append(incident)
        return incident
        
    def escalate(self, incident_id: str, new_severity: str) -> bool:
        for inc in self.incidents:
            if inc.incident_id == incident_id:
                inc.severity = new_severity
                return True
        return False
        
    def resolve(self, incident_id: str, timestamp: datetime) -> bool:
        for inc in self.incidents:
            if inc.incident_id == incident_id:
                inc.status = "RESOLVED"
                inc.resolved_at = timestamp
                return True
        return False
