from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class LegalDocument(BaseModel):
    document_id: str
    jurisdiction: str
    effective_from: datetime
    effective_until: Optional[datetime] = None
    version: int

class RegulatoryObligation(BaseModel):
    obligation_id: str
    jurisdiction: str
    applicable_entity: str
    requirement: str

class RegulatoryEvidence(BaseModel):
    evidence_id: str
    source_type: str
    observed_at: datetime
    integrity_status: str # VERIFIED, UNVERIFIED, INVALID

class ComplianceAssessment(BaseModel):
    assessment_id: str
    obligation_id: str
    entity_id: str
    status: str # COMPLIANT, NON_COMPLIANT, INSUFFICIENT_EVIDENCE, REQUIRES_HUMAN_REVIEW
    evidence_ids: List[str]
