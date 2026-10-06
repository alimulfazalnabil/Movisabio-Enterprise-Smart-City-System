from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import enum

class SituationStatus(str, enum.Enum):
    DETECTED = "DETECTED"
    ACTIVE = "ACTIVE"
    ESCALATING = "ESCALATING"
    STABILIZING = "STABILIZING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class Situation(BaseModel):
    situation_id: str
    tenant_id: str
    type: str
    severity: str
    status: SituationStatus
    evidence_events: List[str]
    confidence: float
    detected_at: datetime
    
class SituationEngine:
    def __init__(self):
        self.active_situations: Dict[str, Situation] = {}
        
    def evaluate_correlation(self, events: List[Dict]) -> Optional[Situation]:
        """
        Correlates multiple domain events into a unified Territorial Situation.
        """
        # Cross-domain fusion logic
        weather_events = [e for e in events if e.get("domain") == "weather"]
        traffic_events = [e for e in events if e.get("domain") == "traffic"]
        
        if weather_events and traffic_events:
            situation = Situation(
                situation_id=f"sit-{int(datetime.now().timestamp())}",
                tenant_id="tenant-1",
                type="WEATHER_TRAFFIC_DISRUPTION",
                severity="HIGH",
                status=SituationStatus.ACTIVE,
                evidence_events=[e["event_id"] for e in events],
                confidence=0.88,
                detected_at=datetime.now()
            )
            self.active_situations[situation.situation_id] = situation
            return situation
            
        return None
