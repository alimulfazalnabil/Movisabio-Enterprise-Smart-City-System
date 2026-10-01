import pytest
from src.services.ai_fabric.engine.orchestrator import AgentOrchestrator

def test_orchestrator_conflict_resolution():
    orchestrator = AgentOrchestrator()
    
    proposals = [
        {"agent": "TRAFFIC_AI", "domain": "TRAFFIC", "action": "INCREASE_THROUGHPUT"},
        {"agent": "ENVIRONMENT_AI", "domain": "ENVIRONMENT", "action": "REDUCE_IDLING"},
        {"agent": "EMERGENCY_AI", "domain": "EMERGENCY", "action": "CLEAR_CORRIDOR_FOR_AMBULANCE"},
        {"agent": "TRANSIT_AI", "domain": "TRANSIT", "action": "PRIORITIZE_BUS"}
    ]
    
    # Emergency should override all others based on the deterministic hierarchy
    winner = orchestrator.resolve_conflict(proposals)
    
    assert winner["agent"] == "EMERGENCY_AI"
    assert winner["action"] == "CLEAR_CORRIDOR_FOR_AMBULANCE"

def test_orchestrator_transit_over_traffic():
    orchestrator = AgentOrchestrator()
    
    proposals = [
        {"agent": "TRAFFIC_AI", "domain": "TRAFFIC", "action": "INCREASE_THROUGHPUT"},
        {"agent": "TRANSIT_AI", "domain": "TRANSIT", "action": "PRIORITIZE_BUS"}
    ]
    
    winner = orchestrator.resolve_conflict(proposals)
    
    assert winner["agent"] == "TRANSIT_AI"
