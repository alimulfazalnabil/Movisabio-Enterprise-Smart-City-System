from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class AnomalyCandidate(BaseModel):
    anomaly_id: str
    anomaly_type: str
    entity_id: str
    score: float
    baseline_reference: Dict[str, Any]
    detected_at: datetime
    
class AnomalyEnsemble:
    def __init__(self):
        self.models = ["statistical_ewma", "isolation_forest", "temporal_baseline"]
        
    def detect_anomalies(self, entity_id: str, current_value: float, context: Dict) -> Optional[AnomalyCandidate]:
        """
        Runs multiple anomaly detection models and votes to reduce false positives.
        """
        # Simulated ensemble evaluation
        votes = 0
        baseline_expected = context.get("historical_average", 0)
        
        if current_value > baseline_expected * 1.5:
            votes += 1 # Statistical vote
            
        if context.get("is_holiday") is False and current_value > baseline_expected * 1.2:
            votes += 1 # Contextual/Temporal vote
            
        if votes >= 2:
            return AnomalyCandidate(
                anomaly_id=f"anom-{int(datetime.now().timestamp())}",
                anomaly_type="STATISTICAL_DEVIATION",
                entity_id=entity_id,
                score=0.85,
                baseline_reference={"expected": baseline_expected, "observed": current_value},
                detected_at=datetime.now()
            )
            
        return None
