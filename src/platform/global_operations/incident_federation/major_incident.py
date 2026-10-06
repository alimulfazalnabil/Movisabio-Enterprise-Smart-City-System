from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class GlobalIncidentStatus(str, enum.Enum):
    ASSESSING = "ASSESSING"
    COORDINATING = "COORDINATING"
    REMEDIATING = "REMEDIATING"
    RESOLVED = "RESOLVED"

class MajorIncident(BaseModel):
    global_incident_id: str
    title: str
    impacted_regions: List[str]
    status: GlobalIncidentStatus = GlobalIncidentStatus.ASSESSING
    regional_incident_refs: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GlobalIncidentEngine:
    def __init__(self):
        self.major_incidents: Dict[str, MajorIncident] = {}
        
    def declare_major_incident(self, incident: MajorIncident) -> MajorIncident:
        self.major_incidents[incident.global_incident_id] = incident
        return incident
        
    def add_impacted_region(self, global_incident_id: str, region_id: str, regional_incident_ref: str) -> MajorIncident:
        if global_incident_id not in self.major_incidents:
            raise ValueError("Global incident not found")
            
        incident = self.major_incidents[global_incident_id]
        if region_id not in incident.impacted_regions:
            incident.impacted_regions.append(region_id)
        if regional_incident_ref not in incident.regional_incident_refs:
            incident.regional_incident_refs.append(regional_incident_ref)
            
        return incident
