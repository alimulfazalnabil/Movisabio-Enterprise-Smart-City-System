from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class PartnerStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    APPROVED = "APPROVED"
    CERTIFIED = "CERTIFIED"
    SUSPENDED = "SUSPENDED"

class EcosystemPartner(BaseModel):
    partner_id: str
    name: str
    partner_type: str
    status: PartnerStatus = PartnerStatus.APPLIED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PartnerRegistry:
    def __init__(self):
        self.partners: Dict[str, EcosystemPartner] = {}
        
    def register_partner(self, partner: EcosystemPartner) -> EcosystemPartner:
        self.partners[partner.partner_id] = partner
        return partner
        
    def approve_partner(self, partner_id: str) -> EcosystemPartner:
        if partner_id not in self.partners:
            raise ValueError("Partner not found")
        self.partners[partner_id].status = PartnerStatus.APPROVED
        return self.partners[partner_id]
