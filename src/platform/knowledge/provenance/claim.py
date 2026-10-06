from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import enum

class EvidenceTier(str, enum.Enum):
    AUTHORITATIVE_RECORD = "AUTHORITATIVE_RECORD"
    VERIFIED_SENSOR = "VERIFIED_SENSOR"
    VERIFIED_FIELD_OBSERVATION = "VERIFIED_FIELD_OBSERVATION"
    SCIENTIFIC_DATA = "SCIENTIFIC_DATA"
    VALIDATED_MODEL_OUTPUT = "VALIDATED_MODEL_OUTPUT"
    AI_INFERENCE = "AI_INFERENCE"
    UNVERIFIED_REPORT = "UNVERIFIED_REPORT"

class KnowledgeClaim(BaseModel):
    claim_id: str
    subject_id: str
    predicate: str
    object_value: str
    confidence: float
    evidence_tier: EvidenceTier
    sources: List[str]
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class ProvenanceEngine:
    def verify_claim(self, claim: KnowledgeClaim, minimum_tier: EvidenceTier) -> bool:
        """
        Ensures a claim meets the minimum required evidence tier.
        """
        tier_hierarchy = [
            EvidenceTier.UNVERIFIED_REPORT,
            EvidenceTier.AI_INFERENCE,
            EvidenceTier.VALIDATED_MODEL_OUTPUT,
            EvidenceTier.SCIENTIFIC_DATA,
            EvidenceTier.VERIFIED_FIELD_OBSERVATION,
            EvidenceTier.VERIFIED_SENSOR,
            EvidenceTier.AUTHORITATIVE_RECORD
        ]
        claim_idx = tier_hierarchy.index(claim.evidence_tier)
        min_idx = tier_hierarchy.index(minimum_tier)
        return claim_idx >= min_idx
