from sqlalchemy import Column, String, JSON, DateTime
from src.core.models import BaseEntity, generate_ulid_like_id

class AuditEvent(BaseEntity):
    """
    Immutable system-wide audit trail.
    """
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("adt"))
    
    event_type = Column(String, index=True, nullable=False) # e.g. traffic_signal_command, login, user_creation
    actor_id = Column(String, index=True, nullable=False)
    
    # Target resource references
    target_resource_id = Column(String, index=True, nullable=True)
    target_resource_type = Column(String, nullable=True)
    
    action = Column(String, nullable=False)
    
    previous_state = Column(JSON, nullable=True)
    requested_state = Column(JSON, nullable=True)
    
    result = Column(String, nullable=False) # accepted, rejected, failed
    
    # Overriding created_at from BaseEntity to mean the exact event occurrence
    occurred_at = Column(DateTime(timezone=True), nullable=False)
