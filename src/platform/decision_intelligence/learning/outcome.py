from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class DecisionOutcome(BaseModel):
    outcome_id: str
    decision_id: str
    expected_metrics: Dict[str, float]
    actual_metrics: Dict[str, float]
    outcome_status: str
    observed_at: datetime
    
class DecisionLearner:
    def evaluate_outcome(self, outcome: DecisionOutcome) -> Dict[str, float]:
        """
        Calculates deviation between expected and actual metrics for continuous learning.
        """
        deviations = {}
        for key, expected_val in outcome.expected_metrics.items():
            actual_val = outcome.actual_metrics.get(key)
            if actual_val is not None and expected_val != 0:
                deviation = (actual_val - expected_val) / expected_val
                deviations[key] = deviation
                
        return deviations
