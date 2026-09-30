import pytest
from src.signal_control.safety_gate import SafetyGate

def test_min_green_violation():
    gate = SafetyGate()
    state = {"elapsed_time": 5} # Below min_green of 10
    
    result = gate.validate_command(state, "NEXT_PHASE", {})
    assert result["status"] == "REJECTED"
    assert result["reason"] == "MIN_GREEN_VIOLATION"

def test_safe_transition():
    gate = SafetyGate()
    state = {"elapsed_time": 15} # Above min_green of 10
    
    result = gate.validate_command(state, "NEXT_PHASE", {})
    assert result["status"] == "APPROVED"
    assert result["reason"] == "SAFE_TRANSITION"

def test_max_green_violation():
    gate = SafetyGate()
    state = {"elapsed_time": 115} 
    
    # 115 + 10 = 125, which exceeds max_green of 120
    result = gate.validate_command(state, "EXTEND_GREEN", {"seconds": 10})
    assert result["status"] == "REJECTED"
    assert result["reason"] == "MAX_GREEN_VIOLATION"
