from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone

class Organization(BaseModel):
    org_id: str
    name: str
    customer_type: str # MUNICIPALITY, ENTERPRISE, etc.
    status: str = "ACTIVE"
    created_at: datetime

class Tenant(BaseModel):
    tenant_id: str
    org_id: str
    name: str
    region_id: str
    status: str = "PROVISIONING" # ACTIVE, SUSPENDED, TERMINATED
    created_at: datetime

class TenantRegistry:
    def __init__(self):
        self.organizations: Dict[str, Organization] = {}
        self.tenants: Dict[str, Tenant] = {}
        
    def register_organization(self, org: Organization) -> None:
        self.organizations[org.org_id] = org
        
    def register_tenant(self, tenant: Tenant) -> None:
        self.tenants[tenant.tenant_id] = tenant
        
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        return self.tenants.get(tenant_id)
