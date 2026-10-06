from pydantic import BaseModel
from typing import List, Optional

class SessionContext(BaseModel):
    user_id: str
    tenant_id: str
    organization_id: str
    role: str # e.g. TRAFFIC_OPERATOR, CITIZEN, EXECUTIVE
    jurisdiction_id: str
    region_id: str
    permissions: List[str]
    data_classification_scope: List[str]
    
    def can_access(self, required_permission: str) -> bool:
        return required_permission in self.permissions
