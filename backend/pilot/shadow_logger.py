import json
import uuid
from datetime import datetime
from typing import Dict, Any

class ShadowModeLogger:
    """
    Logs AI recommendations without executing them on physical hardware.
    Used to generate the Pilot Evidence Package.
    """
    def __init__(self, log_path: str = "shadow_pilot.jsonl"):
        self.log_path = log_path
        
    def log_recommendation(
        self,
        intersection_id: str,
        current_state: Dict,
        prediction: Dict,
        recommended_action: str,
        safety_status: str,
        model_version: str
    ):
        entry = {
            "audit_id": f"SHADOW-{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.utcnow().isoformat(),
            "intersection": intersection_id,
            "traffic_state": current_state,
            "prediction_forecast": prediction,
            "recommended_action": recommended_action,
            "safety_result": safety_status,
            "execution": "SKIPPED_SHADOW_MODE",
            "model_version": model_version
        }
        
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
        return entry
