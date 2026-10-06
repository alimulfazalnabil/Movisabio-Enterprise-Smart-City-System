from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime, timezone
import hashlib

class Evidence(BaseModel):
    evidence_id: str
    control_id: str
    source_system: str
    artifact_uri: str
    content_hash: str
    created_at: datetime
    verification_status: str = "PENDING"

class EvidenceStore:
    def __init__(self):
        self.evidence: Dict[str, Evidence] = {}
        
    def submit_evidence(self, control_id: str, source_system: str, artifact_uri: str, content: bytes) -> str:
        evidence_id = f"evd-{len(self.evidence) + 1}"
        content_hash = hashlib.sha256(content).hexdigest()
        
        evidence = Evidence(
            evidence_id=evidence_id,
            control_id=control_id,
            source_system=source_system,
            artifact_uri=artifact_uri,
            content_hash=content_hash,
            created_at=datetime.now(timezone.utc)
        )
        self.evidence[evidence_id] = evidence
        return evidence_id
        
    def verify_evidence(self, evidence_id: str) -> bool:
        if evidence_id in self.evidence:
            self.evidence[evidence_id].verification_status = "VERIFIED"
            return True
        return False
