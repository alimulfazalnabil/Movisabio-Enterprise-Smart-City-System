from sqlalchemy import Column, String, DateTime, func, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from platform.database.session import Base
import uuid
import enum

class RoleEnum(str, enum.Enum):
    PLATFORM_ADMIN = "Platform Admin"
    CITY_ADMIN = "City Admin"
    TRAFFIC_MANAGER = "Traffic Manager"
    OPERATOR = "Traffic Operator"
    ANALYST = "Data Analyst"
    RESEARCHER = "Researcher"
    AUDITOR = "Auditor"
    READ_ONLY = "Read Only"

class User(Base):
    """
    SaaS User model with Tenant isolation and RBAC.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False, index=True)
    
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    
    role = Column(Enum(RoleEnum), default=RoleEnum.READ_ONLY, nullable=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    tenant = relationship("Tenant")
