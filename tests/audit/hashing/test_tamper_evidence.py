import pytest
from src.audit.models import AuditEvent, ActorType

def test_audit_event_tamper_evidence_hash():
    # Simulate two events
    event1 = AuditEvent(
        id="evt_1",
        event_type="traffic.command.requested",
        tenant_id="tenant_A",
        actor_type=ActorType.USER,
        actor_id="user_123",
        resource_type="intersection",
        resource_id="int_01",
        action="traffic.control",
        result="SUCCESS"
    )
    
    hash1 = event1.compute_hash()
    assert hash1 is not None
    event1.event_hash = hash1
    
    event2 = AuditEvent(
        id="evt_2",
        event_type="traffic.command.executed",
        tenant_id="tenant_A",
        actor_type=ActorType.SYSTEM,
        actor_id="sys_controller",
        resource_type="intersection",
        resource_id="int_01",
        action="traffic.control",
        result="SUCCESS",
        previous_event_hash=hash1
    )
    
    hash2 = event2.compute_hash()
    assert hash2 is not None
    assert hash1 != hash2
    
    # Tampering test: modify event1's result maliciously
    event1.result = "DENIED"
    tampered_hash = event1.compute_hash()
    
    assert tampered_hash != hash1, "Tampering must invalidate the hash"
