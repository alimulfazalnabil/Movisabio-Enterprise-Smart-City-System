from datetime import datetime, timezone, timedelta
from src.platform.identity.models import MoviIdentity, AIAgentIdentity
from src.platform.access_control.abac import AccessRequest
from src.platform.policy_engine.pdp import PolicyDecisionPoint

def test_pdp_cross_tenant_denial():
    pdp = PolicyDecisionPoint(policy_version="1.0")
    
    subject = MoviIdentity(
        identity_id="user-123",
        identity_type="HUMAN",
        tenant_id="tenant-A",
        status="ACTIVE",
        roles=["operator"],
        trust_level="HIGH",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    request = AccessRequest(
        subject=subject,
        action="traffic.signal.override",
        resource_id="signal-123",
        resource_type="TRAFFIC_SIGNAL",
        tenant_id="tenant-B", # Different tenant
        purpose="emergency_routing"
    )
    
    decision = pdp.evaluate(request)
    assert decision.decision == "DENY"
    assert "CROSS_TENANT_DENIED" in decision.conditions

def test_pdp_ai_agent_forbidden_capability():
    pdp = PolicyDecisionPoint(policy_version="1.0")
    
    agent = AIAgentIdentity(
        identity_id="agent-123",
        identity_type="AI_AGENT",
        tenant_id="tenant-A",
        status="ACTIVE",
        roles=[],
        trust_level="HIGH",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        risk_class="R4",
        capabilities=["traffic.read"],
        forbidden_capabilities=["traffic.signal.control.execute"],
        model_version="v1.0",
        policy_version="1.0"
    )
    
    # AI tries to execute direct control
    request = AccessRequest(
        subject=agent,
        action="traffic.signal.control.execute",
        resource_id="signal-123",
        resource_type="TRAFFIC_SIGNAL",
        tenant_id="tenant-A",
        purpose="traffic_optimization"
    )
    
    decision = pdp.evaluate(request)
    assert decision.decision == "DENY"
    assert "AGENT_ACTION_FORBIDDEN" in decision.conditions

def test_pdp_ai_agent_allow_capability():
    pdp = PolicyDecisionPoint(policy_version="1.0")
    
    agent = AIAgentIdentity(
        identity_id="agent-123",
        identity_type="AI_AGENT",
        tenant_id="tenant-A",
        status="ACTIVE",
        roles=[],
        trust_level="HIGH",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        risk_class="R4",
        capabilities=["traffic.read"],
        forbidden_capabilities=["traffic.signal.control.execute"],
        model_version="v1.0",
        policy_version="1.0"
    )
    
    # AI reads traffic
    request = AccessRequest(
        subject=agent,
        action="traffic.read",
        resource_id="intersection-123",
        resource_type="INTERSECTION",
        tenant_id="tenant-A",
        purpose="traffic_optimization"
    )
    
    decision = pdp.evaluate(request)
    assert decision.decision == "ALLOW"
