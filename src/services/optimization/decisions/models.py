from typing import Dict, Any, Optional
from pydantic import BaseModel

class RecommendedAction(BaseModel):
    type: str # e.g., 'HOLD', 'EXTEND_GREEN', 'TERMINATE', 'CHANGE_PHASE'
    duration_seconds: Optional[int] = None
    target_phase: Optional[str] = None

class OptimizationModel(BaseModel):
    name: str
    version: str

class OptimizationDecision(BaseModel):
    """
    Candidate Action Recommendation.
    Must be validated by the Safety Engine before becoming a command.
    """
    optimization_id: str
    intersection_id: str
    current_phase: str
    
    recommended_action: RecommendedAction
    reason: Dict[str, Any]
    
    model: OptimizationModel
    confidence: float
    status: str = "CANDIDATE" # Moves to APPROVED or REJECTED after safety evaluation
