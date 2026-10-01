import enum
import hashlib
import json
from sqlalchemy import Column, String, Boolean, Enum, JSON, DateTime
from src.core.models import BaseEntity, generate_ulid_like_id
from datetime import datetime

class ActorType(str, enum.Enum):
    USER = "USER"
    SERVICE = "SERVICE"
    DEVICE = "DEVICE"
    API_KEY = "API_KEY"
    SYSTEM = "SYSTEM"
    AI_AGENT = "AI_AGENT"

class AuditEvent(BaseEntity):
    """
    Immutable audit ledger for security, traffic, and compliance tracking.
    """
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("evt"))
    
    event_type = Column(String, index=True, nullable=False)
    event_version = Column(String, default="1", nullable=False)
    
    # Context
    actor_type = Column(Enum(ActorType), nullable=False)
    actor_id = Column(String, index=True, nullable=False)
    
    resource_type = Column(String, index=True, nullable=True)
    resource_id = Column(String, index=True, nullable=True)
    
    action = Column(String, nullable=False)
    result = Column(String, nullable=False) # SUCCESS / DENIED / FAILED
    
    request_id = Column(String, index=True, nullable=True)
    correlation_id = Column(String, index=True, nullable=True)
    
    service_name = Column(String, nullable=True)
    service_instance = Column(String, nullable=True)
    
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    metadata_payload = Column(JSON, nullable=True)
    
    # Tamper evidence
    previous_event_hash = Column(String, nullable=True)
    event_hash = Column(String, nullable=True)

    def compute_hash(self) -> str:
        """
        Computes the SHA-256 hash of the canonical event + previous hash.
        """
        canonical = json.dumps({
            "id": self.id,
            "event_type": self.event_type,
            "tenant_id": self.tenant_id,
            "actor": self.actor_id,
            "resource": self.resource_id,
            "result": self.result,
            "previous_hash": self.previous_event_hash
        }, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()
