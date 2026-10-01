from typing import Optional, Dict, Any, List
from src.audit.models import AuditEvent, ActorType
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger("movisabio.audit")

class AuditService:
    """
    Enterprise Audit Pipeline for MoviSabio.
    """
    
    @staticmethod
    def log_event(
        db: Session,
        event_type: str,
        actor_type: ActorType,
        actor_id: str,
        action: str,
        result: str,
        tenant_id: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        service_name: str = "movisabio-api"
    ) -> AuditEvent:
        """
        Records an immutable audit event with tamper-evident hashing.
        """
        # In a high-volume production scenario, this might push to Kafka/PubSub instead of blocking on DB.
        # Here we model the direct-to-DB synchronous insertion.
        
        # Determine previous event hash for the tenant's partition (simplified here)
        # Normally we query the latest event for this tenant
        previous_event = db.query(AuditEvent).filter(AuditEvent.tenant_id == tenant_id).order_by(AuditEvent.created_at.desc()).first()
        previous_hash = previous_event.event_hash if previous_event else None
        
        event = AuditEvent(
            event_type=event_type,
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            result=result,
            tenant_id=tenant_id,
            resource_type=resource_type,
            resource_id=resource_id,
            request_id=request_id,
            correlation_id=correlation_id,
            metadata_payload=metadata,
            service_name=service_name,
            previous_event_hash=previous_hash
        )
        
        # Generate the hash
        event.event_hash = event.compute_hash()
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        # In a real environment, also stream to SIEM via an asynchronous task or logger
        logger.info(f"Audit event recorded: {event.id} ({event.event_type})")
        
        return event

    @staticmethod
    def query_events(
        db: Session,
        tenant_id: str,
        event_type: Optional[str] = None,
        actor_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditEvent]:
        """
        Queries audit events securely bounded by tenant.
        """
        query = db.query(AuditEvent).filter(AuditEvent.tenant_id == tenant_id)
        
        if event_type:
            query = query.filter(AuditEvent.event_type == event_type)
        if actor_id:
            query = query.filter(AuditEvent.actor_id == actor_id)
        if resource_id:
            query = query.filter(AuditEvent.resource_id == resource_id)
            
        return query.order_by(AuditEvent.created_at.desc()).limit(limit).all()
