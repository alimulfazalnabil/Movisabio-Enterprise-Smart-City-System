from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import hashlib

class Location(BaseModel):
    lat: float
    lon: float

class MobileEvidence(BaseModel):
    evidence_id: str
    task_id: str
    asset_id: str
    captured_at: datetime
    device_id: str
    operator_id: str
    location: Location
    type: str # PHOTO, VIDEO, SENSOR
    data_hash: str
    digital_signature: Optional[str] = None
    sync_status: str = "PENDING"
    
    def verify_integrity(self, raw_data: bytes) -> bool:
        """
        Cryptographically verifies that the evidence was not tampered with offline.
        """
        calculated = hashlib.sha256(raw_data).hexdigest()
        return calculated == self.data_hash
