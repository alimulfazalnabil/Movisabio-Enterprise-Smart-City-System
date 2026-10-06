from typing import Dict, Any, Optional
from datetime import datetime, timezone
import uuid
from backend.app.models.traffic import OperatingModeEnum, Incident

class PilotManager:
    """
    B7 - Pilot Readiness and Operating Mode Manager
    Governs transitions between SHADOW, ASSISTED, and AUTOMATIC modes.
    """
    def __init__(self):
        self.active_modes: Dict[str, OperatingModeEnum] = {}
        self.incidents: Dict[str, Any] = {}

    def get_mode(self, intersection_id: str) -> OperatingModeEnum:
        return self.active_modes.get(intersection_id, OperatingModeEnum.OFF)

    def request_mode_transition(self, intersection_id: str, new_mode: OperatingModeEnum, operator_id: str, authorization_token: str) -> bool:
        # B7.21 Transitions must be governed
        current_mode = self.get_mode(intersection_id)
        
        # Example hardcoded rules for transition
        if new_mode == OperatingModeEnum.AUTHORIZED_AUTOMATIC:
            if current_mode not in [OperatingModeEnum.LIMITED_AUTOMATIC, OperatingModeEnum.ASSISTED]:
                print(f"Transition Reject: Must step through ASSISTED/LIMITED before {new_mode.value}")
                return False
                
        self.active_modes[intersection_id] = new_mode
        print(f"Intersection {intersection_id} transitioned to {new_mode.value} by {operator_id}")
        return True

    def report_incident(self, intersection_id: str, severity: str, description: str, detected_by: str) -> str:
        # B7.17 Incident Management
        incident_id = f"INC-{str(uuid.uuid4())[:8].upper()}"
        
        self.incidents[incident_id] = {
            "intersection_id": intersection_id,
            "severity": severity,
            "description": description,
            "detected_by": detected_by,
            "timestamp": datetime.now(timezone.utc),
            "status": "OPEN"
        }
        
        # B7.9 Real-Time Incident Detection -> Auto trigger failsafe/shadow for High/Critical
        if severity in ["P1 Critical", "P2 High"]:
            print(f"CRITICAL INCIDENT {incident_id}. Triggering Rollback/Failsafe.")
            self.trigger_rollback(intersection_id)
            
        return incident_id

    def trigger_rollback(self, intersection_id: str):
        # B7.22 Pilot Rollback
        self.active_modes[intersection_id] = OperatingModeEnum.FAILSAFE
        print(f"Rollback executed for {intersection_id}. Returning to native controller plan.")
