import pytest
from backend.app.safety.engine import SafetyEngine
from backend.app.traffic.optimizer import TrafficOptimizer

def test_safety_min_green_violation():
    engine = SafetyEngine({"min_green": 10.0})
    current_state = {"phase": "NS_GREEN", "elapsed": 5.0}
    proposed = {"recommended_phase": "EW_GREEN", "duration": 30.0}
    
    result = engine.validate_command(current_state, proposed)
    assert result["status"] == "REJECTED"
    assert "MIN_GREEN_VIOLATION" in result["reason"]

def test_safety_max_green_violation():
    engine = SafetyEngine({"max_green": 60.0})
    current_state = {"phase": "NS_GREEN", "elapsed": 15.0}
    proposed = {"recommended_phase": "NS_GREEN", "duration": 70.0}
    
    result = engine.validate_command(current_state, proposed)
    assert result["status"] == "REJECTED"
    assert "MAX_GREEN_VIOLATION" in result["reason"]
    
def test_baseline_optimizer():
    optimizer = TrafficOptimizer(mode="baseline")
    traffic_state = {
        "lane_states": {
            "N1": {"instantaneous_count": 10},
            "E1": {"instantaneous_count": 2}
        }
    }
    signal_state = {"phase": "EW_GREEN", "remaining": 5.0}
    
    result = optimizer.optimize(traffic_state, signal_state)
    assert result["recommended_phase"] == "NS_GREEN"
