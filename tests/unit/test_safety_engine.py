import pytest
from services.safety.engine import SafetyEngine
from services.optimization.rule_based import SignalDecision

def test_safety_engine_rejects_conflicting_green():
    engine = SafetyEngine()
    
    # AI wants to turn North-South GREEN
    decision = SignalDecision(
        intersection_id="ID_01",
        desired_phase="North-South",
        desired_state="GREEN",
        reason="AI optimization"
    )
    
    # But the East-West phase is currently GREEN
    current_state = {"conflicting_phase": "GREEN"}
    
    result = engine.validate_decision(decision, current_state)
    
    assert result.is_safe is False
    assert result.permitted_state == "RED"
    assert "Conflict matrix violation" in result.reason

def test_safety_engine_allows_safe_transition():
    engine = SafetyEngine()
    
    # AI wants to turn North-South GREEN
    decision = SignalDecision(
        intersection_id="ID_01",
        desired_phase="North-South",
        desired_state="GREEN",
        reason="AI optimization"
    )
    
    # Conflicting phases are safely RED
    current_state = {"conflicting_phase": "RED"}
    
    result = engine.validate_decision(decision, current_state)
    
    assert result.is_safe is True
    assert result.permitted_state == "GREEN"
