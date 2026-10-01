from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class AgentRiskClass(str, Enum):
    R0_INFORMATIONAL = "R0"
    R1_ANALYTICAL = "R1"
    R2_DECISION_SUPPORT = "R2"
    R3_OPERATIONAL_RECOMMENDATION = "R3"
    R4_SAFETY_CRITICAL = "R4"
    R5_PHYSICAL_CONTROL = "R5"

class AgentRegistry(BaseModel):
    agent_id: str
    name: str
    domain: str
    version: str
    description: str
    capabilities: List[str]
    risk_class: AgentRiskClass
    status: str # LIVE, SHADOW, DISABLED

class AgentMessage(BaseModel):
    message_id: str
    message_type: str
    sender_agent: str
    receiver_agent: Optional[str] = None
    tenant_id: str
    territory_id: str
    timestamp: datetime
    payload: Dict[str, Any]
    confidence: float

class AgentDecisionRecord(BaseModel):
    decision_id: str
    agent_id: str
    tenant_id: str
    territory_id: str
    trigger_event: str
    input_context: Dict[str, Any]
    reasoning_summary: str
    recommendation: Dict[str, Any]
    confidence: float
    authorization_status: str # AWAITING, APPROVED, REJECTED
    final_action: Optional[str] = None
