import pytest
from src.services.ai_fabric.engine.safety import AgentSafetyGateway

def test_safety_gateway_allows_valid_candidate():
    gateway = AgentSafetyGateway()
    
    candidate = {"target": "INT-1", "action": "EXTEND_GREEN", "value": 50}
    hard_constraints = {"max_green_sec": 60}
    
    assert gateway.validate_candidate(candidate, hard_constraints) is True

def test_safety_gateway_rejects_unsafe_candidate():
    gateway = AgentSafetyGateway()
    
    # Agent hallucinated or requested 120 seconds of green, exceeding the 60 second hard limit
    candidate = {"target": "INT-1", "action": "EXTEND_GREEN", "value": 120}
    hard_constraints = {"max_green_sec": 60}
    
    assert gateway.validate_candidate(candidate, hard_constraints) is False
