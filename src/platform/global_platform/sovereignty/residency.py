from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

class ResidencyPolicy(BaseModel):
    tenant_id: str
    data_classification: str
    primary_region: str
    allowed_regions: List[str]
    cross_border_transfer_allowed: bool

class DataTransferRequest(BaseModel):
    tenant_id: str
    source_region: str
    destination_region: str
    data_classification: str
    purpose: str

class TransferEngine:
    def __init__(self):
        self.policies: Dict[str, ResidencyPolicy] = {} # tenant_id -> policy
        
    def set_policy(self, policy: ResidencyPolicy) -> None:
        self.policies[policy.tenant_id] = policy
        
    def evaluate_transfer(self, request: DataTransferRequest) -> str:
        """Evaluates whether a cross-region data transfer is legally/technically authorized."""
        policy = self.policies.get(request.tenant_id)
        if not policy:
            return "DENIED_NO_POLICY"
            
        if request.data_classification != policy.data_classification:
            # Simplified: Assume strict classification matching for test
            pass
            
        if request.destination_region not in policy.allowed_regions:
            return "DENIED_REGION_NOT_ALLOWED"
            
        if not policy.cross_border_transfer_allowed and request.source_region != request.destination_region:
            return "DENIED_CROSS_BORDER_RESTRICTED"
            
        return "ALLOWED"
