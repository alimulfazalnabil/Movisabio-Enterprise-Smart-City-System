from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class DecisionEvidence(BaseModel):
    decision_id: str
    agent_id: str
    model_version: str
    input_snapshot: Dict[str, Any] = Field(default_factory=dict)
    confidence: float
    alternatives_considered: List[str] = Field(default_factory=list)
    policy_applied: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProvenanceEngine:
    def __init__(self):
        self.evidence_log: Dict[str, DecisionEvidence] = {}
        
    def record_evidence(self, evidence: DecisionEvidence) -> DecisionEvidence:
        self.evidence_log[evidence.decision_id] = evidence
        return evidence
        
    def replay_decision(self, decision_id: str) -> DecisionEvidence:
        if decision_id not in self.evidence_log:
            raise ValueError("Evidence not found")
        return self.evidence_log[decision_id]
