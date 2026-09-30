from sqlalchemy import Column, String, ForeignKey, JSON, DateTime
from src.core.models import BaseEntity, generate_ulid_like_id

class SignalCommand(BaseEntity):
    """
    Immutable record of a signal control command sent to an intersection.
    Crucial for audit, safety validation, and operational history.
    """
    __tablename__ = "signal_commands"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("cmd"))
    intersection_id = Column(String, ForeignKey("intersections.id"), nullable=False)
    controller_id = Column(String, ForeignKey("devices.id"), nullable=False)
    
    requested_by = Column(String, nullable=False) # e.g. ai_optimizer, user_123
    request_source = Column(String, nullable=False) # e.g. MoviSabioEdge, WebDashboard
    
    command_type = Column(String, nullable=False) # SET_PHASE, EXTEND_GREEN, EMERGENCY_PREEMPT
    payload = Column(JSON, nullable=False) # Detailed command instructions
    
    # AI / Safety context
    model_version = Column(String, nullable=True)
    policy_version = Column(String, nullable=True)
    safety_check_version = Column(String, nullable=True)
    
    # Lifecycle Timestamps
    requested_at = Column(DateTime(timezone=True), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    
    # Command Status (PENDING, VALIDATING, APPROVED, SENT, ACKNOWLEDGED, REJECTED, FAILED)
    command_status = Column(String, nullable=False, default="PENDING")
    failure_reason = Column(String, nullable=True)
