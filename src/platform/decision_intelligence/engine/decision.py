from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
import enum

class DecisionStatus(str, enum.Enum):
    CANDIDATE = "CANDIDATE"
    EVALUATED = "EVALUATED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    AUTHORIZED = "AUTHORIZED"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"

class DecisionOption(BaseModel):
    option_id: str
    description: str
    expected_impact: Dict[str, float]
    risk_level: str
    cost: str
    is_recommended: bool = False

class Decision(BaseModel):
    decision_id: str
    decision_type: str
    tenant_id: str
    scope: Dict[str, str]
    objective: Dict[str, str]
    constraints: List[str]
    options: List[DecisionOption] = []
    recommended_option_id: Optional[str] = None
    status: DecisionStatus = DecisionStatus.CANDIDATE
    confidence: Optional[float] = None
    created_at: datetime
    
class DecisionEngine:
    def __init__(self):
        self.active_decisions: Dict[str, Decision] = {}
        
    def evaluate_decision(self, decision: Decision) -> Decision:
        """
        Evaluates options and selects a recommendation based on objectives and constraints.
        """
        if not decision.options:
            return decision
            
        # Simplified evaluation: select option with best primary objective metric
        primary_obj = decision.objective.get("primary")
        if primary_obj:
            best_option = None
            best_score = float('-inf')
            
            for option in decision.options:
                score = option.expected_impact.get(primary_obj, 0.0)
                if score > best_score:
                    best_score = score
                    best_option = option
                    
            if best_option:
                best_option.is_recommended = True
                decision.recommended_option_id = best_option.option_id
                decision.status = DecisionStatus.EVALUATED
                
        return decision
