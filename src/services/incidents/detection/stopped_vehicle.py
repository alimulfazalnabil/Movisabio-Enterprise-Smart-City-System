from datetime import datetime, timezone
import uuid
from typing import Dict, Any, Optional
from src.services.incidents.models.schemas import Incident, IncidentType, IncidentStatus, IncidentSeverity, EvidenceRef

class StoppedVehicleDetector:
    """
    Evaluates trajectory and state evidence to detect stopped vehicles 
    that might be anomalous (e.g. not stopped for a red light).
    """
    
    def evaluate(self, trajectory_data: Dict[str, Any], signal_state: Dict[str, Any]) -> Optional[Incident]:
        
        speed = trajectory_data.get('speed', 100)
        is_isolated = trajectory_data.get('is_isolated', False)
        duration_stopped = trajectory_data.get('duration_stopped', 0)
        lane_id = trajectory_data.get('lane_id')
        
        current_phase = signal_state.get('active_phase', 'UNKNOWN')
        # Simplified: if the phase is GREEN for this lane, vehicles shouldn't be stopped long
        expected_to_stop = (current_phase == 'RED')
        
        if speed < 1.0 and duration_stopped > 10 and not expected_to_stop:
            
            evidence = EvidenceRef(
                evidence_id=f"EVD-{uuid.uuid4().hex[:8].upper()}",
                type="TRAJECTORY",
                source=trajectory_data.get('camera_id', 'UNKNOWN'),
                timestamp=datetime.now(timezone.utc),
                confidence=0.85
            )
            
            return Incident(
                incident_id=f"INC-{uuid.uuid4().hex[:8].upper()}",
                tenant_id="TENANT-001",
                city_id="CITY-001",
                site_id="SITE-001",
                intersection_id=signal_state.get('intersection_id'),
                incident_type=IncidentType.VEHICLE_STOPPED,
                status=IncidentStatus.DETECTED,
                severity=IncidentSeverity.MEDIUM,
                confidence=0.85,
                detected_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                source_ids=[trajectory_data.get('camera_id', 'UNKNOWN')],
                evidence=[evidence],
                affected_lanes=[lane_id] if lane_id else [],
                affected_signal_groups=[],
                description="Vehicle stopped abnormally during green phase."
            )
            
        return None
