from sqlalchemy import Column, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from src.core.models import BaseEntity, generate_ulid_like_id

class PlatformRole(str, enum.Enum):
    PLATFORM_OWNER = "Platform Owner"
    ORG_ADMIN = "Organization Admin"
    CITY_ADMIN = "City Admin"
    TRAFFIC_MANAGER = "Traffic Manager"
    OPERATOR = "Traffic Operator"
    DATA_ANALYST = "Data Analyst"
    RESEARCHER = "Researcher"
    MAINTENANCE = "Maintenance Engineer"
    AUDITOR = "Auditor"
    VIEWER = "Viewer"

class User(BaseEntity):
    """
    Identity entity bounded to a specific tenant.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("user"))
    
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_mfa_enabled = Column(Boolean, default=False)
    
    # Simple role mapping for now (real RBAC typically has separate Permission/UserRole tables)
    role = Column(Enum(PlatformRole), default=PlatformRole.VIEWER, nullable=False)

class AccessGrant(BaseEntity):
    """
    Temporary delegated access or break-glass access log.
    """
    __tablename__ = "access_grants"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("grant"))
    
    subject_id = Column(String, index=True, nullable=False)
    resource_type = Column(String, nullable=True) # e.g. intersection, tenant
    resource_id = Column(String, nullable=True)
    
    permissions = Column(String, nullable=False) # JSON array of permissions
    
    starts_at = Column(String, nullable=False)
    expires_at = Column(String, nullable=False)
    
    granted_by = Column(String, nullable=False)
    revoked_at = Column(String, nullable=True)
