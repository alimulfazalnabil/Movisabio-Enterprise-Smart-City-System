from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class ADRStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"

class ArchitectureDecisionRecord(BaseModel):
    adr_id: str
    project_id: str
    title: str
    context: str
    decision: str
    alternatives_considered: List[str]
    consequences: str
    status: ADRStatus = ADRStatus.PROPOSED
    approver_id: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ArchitectureEngine:
    def __init__(self):
        self.adrs: Dict[str, ArchitectureDecisionRecord] = {}
        
    def submit_adr(self, adr: ArchitectureDecisionRecord) -> ArchitectureDecisionRecord:
        self.adrs[adr.adr_id] = adr
        return adr
        
    def approve_adr(self, adr_id: str, approver_id: str) -> ArchitectureDecisionRecord:
        if adr_id not in self.adrs:
            raise ValueError("ADR not found")
        self.adrs[adr_id].status = ADRStatus.ACCEPTED
        self.adrs[adr_id].approver_id = approver_id
        return self.adrs[adr_id]
