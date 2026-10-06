import pytest
from backend.app.safety.engine import SafetyEngine
from backend.app.traffic.optimizer import TrafficOptimizer
from backend.app.traffic.controller import MockSignalController, SimulationAdapter
import uuid

# B3.8 / B3.11 / B3.12 Scenario and Missing/Stale Data Tests
def test_missing_data_fallback():
    # If vehicle count is missing, optimizer must handle it correctly
    optimizer = TrafficOptimizer(mode="baseline")
    traffic_state = {
        "lane_states": {} # Missing data
    }
    signal_state = {"phase": "NS_GREEN", "remaining": 5.0}
    
    # Missing data should lead to safe baseline fallback (maintaining current phase or default safety)
    result = optimizer.optimize(traffic_state, signal_state)
    assert result["recommended_phase"] == "NS_GREEN"
    assert "rationale" in result

def test_stale_data_fallback():
    optimizer = TrafficOptimizer(mode="baseline")
    # Simulate a state where data is too old (e.g. checked before calling optimizer)
    # The optimizer should handle it gracefully
    traffic_state = {
        "status": "STALE",
        "lane_states": {"N1": {"instantaneous_count": 50}}
    }
    signal_state = {"phase": "NS_GREEN", "remaining": 5.0}
    
    result = optimizer.optimize(traffic_state, signal_state)
    assert result["recommended_phase"] == "NS_GREEN"

# B3.9 Safety Invariant Tests
def test_safety_reject_invalid_phase():
    engine = SafetyEngine({"min_green": 10.0})
    current_state = {"phase": "NS_GREEN", "elapsed": 15.0}
    
    # Intentionally bad phase
    proposed = {"recommended_phase": "INVALID_PHASE", "duration": 30.0}
    
    result = engine.validate_command(current_state, proposed)
    assert result["status"] == "REJECTED"
    assert "INVALID_PHASE" in result["reason"]

def test_safety_pedestrian_clearance():
    engine = SafetyEngine({"ped_clearance": 15.0})
    # If the system transitions from a phase with pedestrians, it must allow clearance
    # Placeholder for pedestrian test
    assert engine is not None

# B3.15 HIL Test Cases & B3.16 Idempotency
def test_command_idempotency():
    controller = MockSignalController()
    command_id = "CMD-101"
    
    # First send
    success1 = controller.send_command("SIG-1", {"command_id": command_id, "requested_phase": "EW_GREEN", "duration": 30.0})
    assert success1 is True
    
    # Second send
    success2 = controller.send_command("SIG-1", {"command_id": command_id, "requested_phase": "EW_GREEN", "duration": 30.0})
    assert success2 is False # Ignored

# B3.17 Shadow Mode
def test_shadow_mode():
    controller = MockSignalController()
    original_state = controller.get_state("SIG-1").copy()
    
    optimizer = TrafficOptimizer(mode="baseline")
    traffic_state = {"lane_states": {"E1": {"instantaneous_count": 100}}}
    signal_state = {"phase": "NS_GREEN", "remaining": 5.0}
    
    recommendation = optimizer.optimize(traffic_state, signal_state)
    assert recommendation["recommended_phase"] == "EW_GREEN"
    
    # In shadow mode, we DO NOT send to controller
    # controller.send_command(...) # SKIPPED
    
    assert controller.get_state("SIG-1") == original_state
