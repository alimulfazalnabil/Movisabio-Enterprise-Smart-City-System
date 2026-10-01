from datetime import datetime, timezone
from src.services.emergency.models.schemas import EmergencyEvent, Evidence, EmergencyState

class EventCorrelationEngine:
    """
    Evaluates evidence to verify and elevate emergency candidates.
    """
    
    def evaluate_evidence(self, event: EmergencyEvent, new_evidence: Evidence) -> EmergencyEvent:
        event.evidence.append(new_evidence)
        
        # Increase confidence based on evidence type and confidence
        weight = 0.1
        if new_evidence.evidence_type == "OPERATOR_REPORT":
            weight = 0.5
        elif new_evidence.evidence_type in ["CCTV", "SENSOR"]:
            weight = 0.3
            
        event.confidence = min(1.0, event.confidence + (new_evidence.confidence * weight))
        
        # State machine transition logic
        if event.status == EmergencyState.CANDIDATE:
            if event.confidence >= 0.8 or new_evidence.evidence_type == "OPERATOR_REPORT":
                event.status = EmergencyState.VERIFIED
                event.verified_at = datetime.now(timezone.utc)
            elif event.confidence >= 0.5:
                event.status = EmergencyState.CORROBORATING
                
        elif event.status == EmergencyState.CORROBORATING:
            if event.confidence >= 0.8 or new_evidence.evidence_type == "OPERATOR_REPORT":
                event.status = EmergencyState.VERIFIED
                event.verified_at = datetime.now(timezone.utc)
                
        return event
