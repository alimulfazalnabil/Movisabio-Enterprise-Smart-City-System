from typing import Dict, Any, Optional
from datetime import datetime, timezone
from src.services.parking.models.schemas import CurbSegment

class CurbActivityEngine:
    """
    Evaluates vehicle tracks against curb segments to detect 
    candidates for loading, illegal stopping, and double parking.
    """
    
    def evaluate_stop(
        self, 
        curb: CurbSegment, 
        track_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Returns a Candidate Incident dict if rules are violated.
        """
        is_stopped = track_data.get('speed', 100) < 1.0
        duration_stopped = track_data.get('duration_stopped', 0)
        is_within_curb = track_data.get('within_curb_polygon', False)
        is_in_travel_lane = track_data.get('in_travel_lane', False)
        
        if not is_stopped:
            return None
            
        # Check double parking
        if duration_stopped > 30 and not is_within_curb and is_in_travel_lane:
            # Vehicle stopped next to curb but in the active travel lane
            return {
                "type": "DOUBLE_PARKING_CANDIDATE",
                "curb_id": curb.curb_id,
                "confidence": 0.85,
                "timestamp": datetime.now(timezone.utc)
            }
            
        # Check illegal stopping in restricted zones (e.g. BUS_STOP)
        if is_within_curb and 'BUS_STOP' in curb.permitted_use and track_data.get('vehicle_type') != 'BUS':
            if duration_stopped > 15:
                return {
                    "type": "ILLEGAL_STOPPING_CANDIDATE",
                    "curb_id": curb.curb_id,
                    "confidence": 0.90,
                    "timestamp": datetime.now(timezone.utc)
                }
                
        return None
