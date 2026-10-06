from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class DecisionStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ANALYSIS = "ANALYSIS"
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"

class StrategicDecision(BaseModel):
    decision_id: str
    owner: str
    question: str
    options: List[str] = Field(default_factory=list)
    recommendation: Optional[str] = None
    confidence: str = "UNKNOWN"
    status: DecisionStatus = DecisionStatus.DRAFT
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DecisionEngine:
    def __init__(self):
        self.decisions: Dict[str, StrategicDecision] = {}
        
    def create_decision(self, decision: StrategicDecision) -> StrategicDecision:
        self.decisions[decision.decision_id] = decision
        return decision
        
    def recommend(self, decision_id: str, recommendation: str, confidence: str) -> StrategicDecision:
        if decision_id not in self.decisions:
            raise ValueError("Decision not found")
        dec = self.decisions[decision_id]
        if recommendation not in dec.options:
            raise ValueError("Recommendation must be one of the provided options")
        dec.recommendation = recommendation
        dec.confidence = confidence
        dec.status = DecisionStatus.PROPOSED
        return dec
