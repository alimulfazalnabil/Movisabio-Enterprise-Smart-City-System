from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class GlobalTenant(Base):
    """B43.5 - Multi-Tenancy & Tenant Hierarchy"""
    __tablename__ = "global_tenants"
    tenant_id = Column(String, primary_key=True)
    parent_tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"), nullable=True)
    organization_name = Column(String)
    jurisdiction = Column(String)
    deployment_model = Column(String) # SAAS, SOVEREIGN, HYBRID
    data_residency_zone = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TerritoryNode(Base):
    """B43.4 - Territory as a First-Class Entity"""
    __tablename__ = "territory_nodes"
    territory_id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    name = Column(String)
    territory_type = Column(String) # GLOBAL, CONTINENT, NATION, REGION, CITY, DISTRICT
    parent_territory_id = Column(String, ForeignKey("territory_nodes.territory_id"), nullable=True)
    timezone = Column(String)
    currency = Column(String)
    operational_status = Column(String) # DEPLOYING, ACTIVE, DEGRADED, OFFLINE

class FederatedPolicy(Base):
    """B43.9 - Global Policy Framework"""
    __tablename__ = "federated_policies"
    policy_id = Column(String, primary_key=True)
    territory_id = Column(String, ForeignKey("territory_nodes.territory_id"))
    policy_domain = Column(String) # DATA_RESIDENCY, AGENT_AUTONOMY, SECURITY
    configuration_json = Column(JSON)
    is_override = Column(Boolean) # If true, overrides parent policy
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
