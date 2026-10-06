from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class PartnerIntegration(BaseModel):
    integration_id: str
    partner_id: str
    integration_type: str
    environment: str # SANDBOX, PRODUCTION
    status: str
    territory_scope: Optional[Dict] = None
    created_at: datetime

class Partner(BaseModel):
    partner_id: str
    organization_id: str
    name: str
    partner_type: str
    status: str # DISCOVERED, APPROVED, SANDBOX, CERTIFICATION, PRODUCTION, SUSPENDED
    created_at: datetime
