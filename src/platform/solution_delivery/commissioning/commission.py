from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class CommissioningStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    VALIDATED = "VALIDATED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class CommissioningRecord(BaseModel):
    record_id: str
    project_id: str
    site_id: str
    status: CommissioningStatus = CommissioningStatus.PENDING
    checklist_results: Dict[str, bool] = Field(default_factory=dict)
    known_limitations: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CommissioningEngine:
    def __init__(self):
        self.records: Dict[str, CommissioningRecord] = {}
        
    def start_commissioning(self, record: CommissioningRecord) -> CommissioningRecord:
        self.records[record.record_id] = record
        return record
        
    def complete_checklist(self, record_id: str, results: Dict[str, bool], limitations: List[str]) -> CommissioningRecord:
        if record_id not in self.records:
            raise ValueError("Record not found")
        record = self.records[record_id]
        record.checklist_results.update(results)
        record.known_limitations.extend(limitations)
        
        if all(results.values()):
            record.status = CommissioningStatus.VALIDATED
        else:
            record.status = CommissioningStatus.REJECTED
        return record
