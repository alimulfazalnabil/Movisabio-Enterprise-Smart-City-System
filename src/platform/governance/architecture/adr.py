from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import enum

class ADRStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    REVIEW = "REVIEW"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    IMPLEMENTED = "IMPLEMENTED"
    SUPERSEDED = "SUPERSEDED"
    RETIRED = "RETIRED"

class ArchitectureDecisionRecord(BaseModel):
    adr_id: str
    title: str
    decision: str
    context: str
    status: ADRStatus = ADRStatus.PROPOSED
    superseded_by: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC) if hasattr(datetime, 'UTC') else datetime.utcnow())

class ArchitectureAuthority:
    def __init__(self):
        self.adrs: Dict[str, ArchitectureDecisionRecord] = {}
        
    def propose_adr(self, adr: ArchitectureDecisionRecord) -> ArchitectureDecisionRecord:
        self.adrs[adr.adr_id] = adr
        return adr
        
    def review_adr(self, adr_id: str, new_status: ADRStatus, superseding_adr_id: Optional[str] = None) -> ArchitectureDecisionRecord:
        if adr_id not in self.adrs:
            raise ValueError("ADR not found")
        
        adr = self.adrs[adr_id]
        adr.status = new_status
        if superseding_adr_id:
            adr.superseded_by = superseding_adr_id
        return adr
