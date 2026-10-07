from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class OrganizationIdentity(Base):
    """B26.3 - Organization Identity"""
    __tablename__ = "organization_identities"
    org_id = Column(String, primary_key=True)
    name = Column(String)
    jurisdiction = Column(String)
    type = Column(String) # GOVERNMENT, ENTERPRISE, RESEARCH
    trust_status = Column(String) # VERIFIED, PENDING, REVOKED

class DataAsset(Base):
    """B26.5 - Data Ownership Model"""
    __tablename__ = "data_assets"
    asset_id = Column(String, primary_key=True)
    name = Column(String)
    owner_org_id = Column(String, ForeignKey("organization_identities.org_id"))
    classification = Column(String) # PUBLIC, INTERNAL, SENSITIVE
    sovereignty_zone = Column(String) # ZONE_A, ZONE_B
    retention_policy_days = Column(Integer)

class DataContract(Base):
    """B26.20 - Data Contracts"""
    __tablename__ = "data_contracts"
    contract_id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("data_assets.asset_id"))
    consumer_org_id = Column(String, ForeignKey("organization_identities.org_id"))
    allowed_purposes = Column(JSON) # e.g. ["RESEARCH", "TRAFFIC_OPTIMIZATION"]
    status = Column(String) # ACTIVE, EXPIRED, REVOKED

class DataUsageLog(Base):
    """B26.24 - Data Usage Ledger"""
    __tablename__ = "data_usage_logs"
    log_id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("data_assets.asset_id"))
    consumer_org_id = Column(String, ForeignKey("organization_identities.org_id"))
    purpose = Column(String)
    timestamp = Column(DateTime(timezone=True))
    result_status = Column(String) # GRANTED, DENIED
