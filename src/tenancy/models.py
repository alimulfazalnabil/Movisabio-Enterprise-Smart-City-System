from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.core.models import BaseEntity, generate_ulid_like_id

class Organization(BaseEntity):
    """
    Top-level organizational entity (e.g., A City Government, A Mobility Enterprise).
    """
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("org"))
    name = Column(String, index=True, nullable=False)
    billing_email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Note: For Organization, tenant_id is often the same as its own id, or null if it's the root.
    # We set tenant_id to be nullable here or handle it carefully, but typically
    # an Organization owns multiple tenants.
    
    tenants = relationship("Tenant", back_populates="organization")

class Tenant(BaseEntity):
    """
    Logical SaaS boundary. A specific operational environment (e.g., City of Campinas operations).
    """
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("tenant"))
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    
    name = Column(String, index=True, nullable=False)
    country_code = Column(String, nullable=False) # e.g. BR, DE, UY
    
    # Overriding tenant_id constraint as this IS the tenant.
    # In practice, tenant_id on this row will match its own id for consistent querying.
    
    organization = relationship("Organization", back_populates="tenants")
