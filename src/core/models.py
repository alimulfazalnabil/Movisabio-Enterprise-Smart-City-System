from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, declared_attr
import datetime
import uuid

Base = declarative_base()

def generate_ulid_like_id(prefix: str):
    """Generates a prefixed ID (e.g. tenant_1234abcd)"""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

class BaseEntity(Base):
    """
    Abstract base class for all enterprise domain models.
    Enforces tenant isolation and audit metadata.
    """
    __abstract__ = True

    id = Column(String, primary_key=True)
    tenant_id = Column(String, index=True, nullable=False) # Multi-tenancy isolation
    
    status = Column(String, default="ACTIVE")
    version = Column(Integer, default=1)
    
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(String, nullable=True) # ID of user/service who created
    updated_by = Column(String, nullable=True) # ID of user/service who updated

    @declared_attr
    def __mapper_args__(cls):
        # Always use version_id_col for optimistic locking where possible
        return {"version_id_col": cls.version}
