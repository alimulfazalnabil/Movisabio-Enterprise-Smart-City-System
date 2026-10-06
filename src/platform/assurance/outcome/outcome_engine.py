from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import enum

class EvidenceType(str, enum.Enum):
    OBSERVED = "OBSERVED"
    VALIDATED = "VALIDATED"
    MODELED = "MODELED"
    SIMULATED = "SIMULATED"
    ESTIMATED = "ESTIMATED"
    PROJECTED = "PROJECTED"
    UNKNOWN = "UNKNOWN"

class OutcomeStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    ACHIEVED = "ACHIEVED"
    PARTIALLY_ACHIEVED = "PARTIALLY_ACHIEVED"
    MISSED = "MISSED"

class CustomerOutcome(BaseModel):
    outcome_id: str
    tenant_id: str
    kpi_name: str
    baseline_value: float
    target_value: float
    current_value: float
    evidence: EvidenceType = EvidenceType.UNKNOWN
    status: OutcomeStatus = OutcomeStatus.NOT_STARTED
    intervention_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OutcomeEngine:
    def __init__(self):
        self.outcomes: Dict[str, CustomerOutcome] = {}
        
    def register_outcome(self, outcome: CustomerOutcome) -> CustomerOutcome:
        self.outcomes[outcome.outcome_id] = outcome
        return outcome
        
    def measure_outcome(self, outcome_id: str, current_value: float, evidence: EvidenceType) -> CustomerOutcome:
        if outcome_id not in self.outcomes:
            raise ValueError("Outcome not found")
            
        outcome = self.outcomes[outcome_id]
        outcome.current_value = current_value
        outcome.evidence = evidence
        
        # Simple evaluation assuming target < baseline (e.g. reduce delay)
        # In a real system, directionality of improvement would be defined per KPI
        progress = (outcome.baseline_value - current_value) / (outcome.baseline_value - outcome.target_value + 1e-9)
        
        if progress >= 1.0:
            outcome.status = OutcomeStatus.ACHIEVED
        elif progress > 0.5:
            outcome.status = OutcomeStatus.PARTIALLY_ACHIEVED
        elif progress > 0.1:
            outcome.status = OutcomeStatus.ON_TRACK
        else:
            outcome.status = OutcomeStatus.AT_RISK
            
        return outcome
