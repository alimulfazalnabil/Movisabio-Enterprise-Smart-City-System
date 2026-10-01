from datetime import datetime, timezone
from src.services.incidents.models.schemas import Incident, IncidentStatus

class IncidentStateMachine:
    """
    Governs the transitions between incident statuses.
    Prevents invalid operational transitions (e.g., CLOSED -> CANDIDATE).
    """
    
    VALID_TRANSITIONS = {
        IncidentStatus.DETECTED: [IncidentStatus.CANDIDATE, IncidentStatus.DISMISSED],
        IncidentStatus.CANDIDATE: [IncidentStatus.CORROBORATING, IncidentStatus.CONFIRMED, IncidentStatus.DISMISSED],
        IncidentStatus.CORROBORATING: [IncidentStatus.CONFIRMED, IncidentStatus.DISMISSED],
        IncidentStatus.CONFIRMED: [IncidentStatus.ACTIVE, IncidentStatus.MITIGATING, IncidentStatus.RESOLVED],
        IncidentStatus.ACTIVE: [IncidentStatus.MITIGATING, IncidentStatus.RESOLVED],
        IncidentStatus.MITIGATING: [IncidentStatus.RESOLVED, IncidentStatus.ACTIVE],
        IncidentStatus.RESOLVED: [IncidentStatus.CLOSED],
        IncidentStatus.CLOSED: [],
        IncidentStatus.DISMISSED: []
    }
    
    @classmethod
    def transition(cls, incident: Incident, next_status: IncidentStatus, actor: str) -> bool:
        if next_status in cls.VALID_TRANSITIONS.get(incident.status, []):
            incident.status = next_status
            incident.updated_at = datetime.now(timezone.utc)
            if next_status == IncidentStatus.RESOLVED:
                incident.resolved_at = datetime.now(timezone.utc)
            # We would normally also append to an audit trail table here
            return True
        return False
