from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class DeveloperApplication(Base):
    """B40.5 - Application Registration"""
    __tablename__ = "developer_applications"
    app_id = Column(String, primary_key=True)
    developer_org_id = Column(String)
    app_name = Column(String)
    environment = Column(String) # SANDBOX, STAGING, PRODUCTION
    requested_scopes = Column(JSON) # e.g. ["mobility:read", "agents:deploy"]
    approved_scopes = Column(JSON)
    rate_limit_tier = Column(String)
    is_active = Column(Boolean, default=True)

class MarketplaceAsset(Base):
    """B40.6 - API, Data, Model, Agent, and Twin Marketplace"""
    __tablename__ = "marketplace_assets"
    asset_id = Column(String, primary_key=True)
    asset_type = Column(String) # API, DATASET, AI_MODEL, AGENT, DIGITAL_TWIN
    publisher_org_id = Column(String)
    asset_name = Column(String)
    version = Column(String)
    access_class = Column(String) # PUBLIC, REGISTERED, LICENSED, RESTRICTED
    approval_status = Column(String) # DRAFT, VALIDATING, SANDBOX, APPROVED, PUBLISHED
    metadata_json = Column(JSON)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class EventSubscription(Base):
    """B40.13 - Event Marketplace"""
    __tablename__ = "event_subscriptions"
    subscription_id = Column(String, primary_key=True)
    app_id = Column(String, ForeignKey("developer_applications.app_id"))
    event_topic = Column(String) # e.g. "traffic.congestion.detected"
    webhook_url = Column(String)
    is_active = Column(Boolean, default=True)
