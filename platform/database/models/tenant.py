from sqlalchemy import Column, String, DateTime, func, Boolean
from platform.database.session import Base
import uuid

class Tenant(Base):
    """
    SaaS Tenant model. Represents a Municipality or Customer Organization.
    """
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True, nullable=False)
    country_code = Column(String, nullable=False) # e.g. "BR", "DE"
    tier = Column(String, default="STARTER") # STARTER, PROFESSIONAL, ENTERPRISE
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
