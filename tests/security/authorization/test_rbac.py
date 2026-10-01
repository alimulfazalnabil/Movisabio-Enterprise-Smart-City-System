import pytest
from src.auth.authorization import AuthorizationService
from src.core.exceptions import PermissionDeniedException, TenantIsolationException
from src.auth.permissions import Permission
import uuid

class MockResource:
    def __init__(self, id: str):
        self.id = id

def test_tenant_isolation_enforced():
    subject = {
        "sub": "user_1",
        "tenant_id": "tenant_A",
        "roles": ["Viewer"]
    }
    
    # Trying to access tenant_B
    with pytest.raises(TenantIsolationException, match="Cross-tenant access is strictly forbidden"):
        AuthorizationService.authorize(
            subject=subject,
            action=Permission.TRAFFIC_READ,
            tenant="tenant_B"
        )

def test_viewer_cannot_control_traffic():
    subject = {
        "sub": "user_1",
        "tenant_id": "tenant_A",
        "roles": ["Viewer"]
    }
    
    with pytest.raises(PermissionDeniedException, match="Missing required permission"):
        AuthorizationService.authorize(
            subject=subject,
            action=Permission.TRAFFIC_CONTROL,
            tenant="tenant_A"
        )

def test_operator_can_control_traffic():
    subject = {
        "sub": "user_1",
        "tenant_id": "tenant_A",
        "roles": ["Traffic Operator"]
    }
    
    # Should not raise any exception
    result = AuthorizationService.authorize(
        subject=subject,
        action=Permission.TRAFFIC_CONTROL,
        tenant="tenant_A"
    )
    assert result is True

def test_ai_service_least_privilege():
    subject = {
        "sub": "service_optimization",
        "tenant_id": "tenant_A",
        "roles": ["AI/ML Engineer"] # Represents the AI scope
    }
    
    # AI can train/deploy models and read traffic
    assert AuthorizationService.authorize(subject, Permission.MODEL_DEPLOY, "tenant_A") is True
    
    # AI CANNOT directly issue control commands
    with pytest.raises(PermissionDeniedException):
        AuthorizationService.authorize(subject, Permission.TRAFFIC_CONTROL, "tenant_A")

def test_resource_scope_isolation():
    subject = {
        "sub": "user_1",
        "tenant_id": "tenant_A",
        "roles": ["Traffic Operator"]
    }
    
    allowed_resource = MockResource("INT-001")
    denied_resource = MockResource("INT-002")
    
    scope = ["INT-001", "INT-003"]
    
    # Access to allowed resource
    assert AuthorizationService.authorize(subject, Permission.TRAFFIC_CONTROL, "tenant_A", allowed_resource, scope) is True
    
    # Access to denied resource
    with pytest.raises(PermissionDeniedException, match="outside permitted scope"):
        AuthorizationService.authorize(subject, Permission.TRAFFIC_CONTROL, "tenant_A", denied_resource, scope)
