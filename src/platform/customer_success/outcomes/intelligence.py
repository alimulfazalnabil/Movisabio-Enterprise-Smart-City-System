from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class AttributionLevel(str, enum.Enum):
    DIRECTLY_MEASURED = "DIRECTLY_MEASURED"
    STRONGLY_ATTRIBUTED = "STRONGLY_ATTRIBUTED"
    PARTIALLY_ATTRIBUTED = "PARTIALLY_ATTRIBUTED"
    MODEL_ESTIMATED = "MODEL_ESTIMATED"
    SIMULATED = "SIMULATED"
    UNKNOWN = "UNKNOWN"

class CustomerOutcome(BaseModel):
    outcome_id: str
    customer_id: str
    objective: str
    metric: str
    baseline: float
    target: float
    observed: Optional[float] = None
    attribution: AttributionLevel = AttributionLevel.UNKNOWN
    evidence: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OutcomeEngine:
    def __init__(self):
        self.outcomes: Dict[str, CustomerOutcome] = {}
        
    def register_outcome(self, outcome: CustomerOutcome) -> CustomerOutcome:
        self.outcomes[outcome.outcome_id] = outcome
        return outcome
        
    def record_measurement(self, outcome_id: str, observed: float, attribution: AttributionLevel, evidence: str) -> CustomerOutcome:
        if outcome_id not in self.outcomes:
            raise ValueError("Outcome not found")
        
        outcome = self.outcomes[outcome_id]
        outcome.observed = observed
        outcome.attribution = attribution
        outcome.evidence = evidence
        return outcome
