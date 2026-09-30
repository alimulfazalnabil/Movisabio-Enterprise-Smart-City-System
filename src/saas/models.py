from sqlalchemy import Column, String, JSON, DateTime
from src.core.models import BaseEntity, generate_ulid_like_id

class Subscription(BaseEntity):
    """
    SaaS subscription plans attached to an Organization.
    """
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("sub"))
    organization_id = Column(String, nullable=False) # FK to organizations
    
    plan_name = Column(String, nullable=False) # e.g. Free, Professional, Enterprise
    features = Column(JSON, nullable=False) # Entitlements array
    
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
