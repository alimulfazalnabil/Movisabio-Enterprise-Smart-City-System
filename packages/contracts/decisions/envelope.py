from pydantic import BaseModel, Field
from typing import Dict, Any

class SafetyValidation(BaseModel):
    status: str

class AuthorizationStatus(BaseModel):
    status: str

class ExecutionStatus(BaseModel):
    status: str

class DecisionEnvelope(BaseModel):
    decision_id: str
    decision_type: str
    subject_id: str
    agent_id: str
    model_version: str
    
    input_context: Dict[str, Any] = Field(default_factory=dict)
    recommendation: Dict[str, Any] = Field(default_factory=dict)
    
    confidence: float
    policy_version: str
    
    safety_validation: SafetyValidation
    authorization: AuthorizationStatus
    execution: ExecutionStatus
