from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AIDecisionRecord(BaseModel):
    decision_id: str
    agent_id: str
    model_id: str
    model_version: str
    input_snapshot: str
    prediction_id: str
    recommendation: str
    confidence: float
    policy_version: str
    safety_result: str
    authorization: str
    final_action: str
    outcome: Optional[str] = None
    created_at: datetime
