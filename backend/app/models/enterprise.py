from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class EnterpriseOrganization(Base):
    """B44.3 - Enterprise Organization Model"""
    __tablename__ = "enterprise_organizations"
    org_id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id")) # Link to B43 GlobalTenant
    legal_name = Column(String)
    org_type = Column(String) # MUNICIPALITY, ENTERPRISE, UTILITY, GOV_AGENCY
    jurisdiction = Column(String)
    billing_entity = Column(String)
    status = Column(String) # ACTIVE, SUSPENDED, OFFBOARDING

class TenantEntitlement(Base):
    """B44.11 - Entitlement Engine"""
    __tablename__ = "tenant_entitlements"
    entitlement_id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    module_name = Column(String) # e.g. "mobility", "environment", "agents"
    tier = Column(String) # COMMUNITY, PROFESSIONAL, ENTERPRISE, SOVEREIGN
    status = Column(String) # ENABLED, DISABLED, EXPIRED
    limits = Column(JSON) # e.g. {"max_twins": 5, "ai_tokens": 1000000}
    expires_at = Column(DateTime)

class UsageMeterLog(Base):
    """B44.8 - Usage Metering"""
    __tablename__ = "usage_meter_logs"
    log_id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    resource_type = Column(String) # API_CALL, AI_INFERENCE, SIMULATION_JOB, DATA_GB
    quantity = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    metadata_json = Column(JSON)

class TenantBillingContract(Base):
    """B44.13 - Contract Management"""
    __tablename__ = "tenant_billing_contracts"
    contract_id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    plan_type = Column(String)
    mrr_usd = Column(Float) # Monthly Recurring Revenue
    overage_allowed = Column(Boolean)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
