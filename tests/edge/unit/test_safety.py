import pytest
from datetime import datetime, timezone
from src.services.edge.models.schemas import ConnectivityState, EdgePolicyCache
from src.services.edge.engine.safety import EdgeSafetyEngine

def test_offline_safety_principle_rejects_if_not_allowed():
    engine = EdgeSafetyEngine()
    
    policy = EdgePolicyCache(
        policy_version="v1",
        signature="sig",
        expires_at=datetime.now(timezone.utc),
        rules={"max_green_seconds": 60},
        offline_ai_control_allowed=False # CRITICAL: Offline AI is explicitly disabled
    )
    
    candidate = {"type": "GREEN_EXTENSION", "value": 30}
    
    # Allowed when online
    assert engine.validate_local_action(candidate, ConnectivityState.ONLINE, policy) is True
    
    # Rejected when offline because offline_ai_control_allowed=False
    assert engine.validate_local_action(candidate, ConnectivityState.OFFLINE, policy) is False

def test_offline_safety_principle_respects_hard_bounds():
    engine = EdgeSafetyEngine()
    
    policy = EdgePolicyCache(
        policy_version="v1",
        signature="sig",
        expires_at=datetime.now(timezone.utc),
        rules={"max_green_seconds": 60},
        offline_ai_control_allowed=True # Offline AI is permitted
    )
    
    # Even though offline AI is allowed, this candidate exceeds the 60s hard limit
    candidate = {"type": "GREEN_EXTENSION", "value": 90}
    
    assert engine.validate_local_action(candidate, ConnectivityState.OFFLINE, policy) is False
