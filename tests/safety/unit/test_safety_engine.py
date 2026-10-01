import pytest
from datetime import datetime, timezone, timedelta
from src.services.optimization.decisions.models import OptimizationDecision, RecommendedAction, OptimizationModel
from src.services.safety.engine.safety import SafetyEngine
from src.services.safety.models.signal import IntersectionConfig, PhaseDefinition, SignalDuration

def setup_test_data():
    config = IntersectionConfig(
        intersection_id="INT-001",
        signal_groups={},
        phases={
            "NS_GREEN": PhaseDefinition(
                phase_id="NS_GREEN",
                name="North/South Green",
                signal_groups=["SG-N-S", "SG-S-N"],
                duration=SignalDuration(min_green=15, max_green=45, yellow=4, all_red=2)
            )
        }
    )
    
    decision = OptimizationDecision(
        optimization_id="OPT-123",
        intersection_id="INT-001",
        current_phase="NS_GREEN",
        recommended_action=RecommendedAction(type="TERMINATE"),
        reason={},
        model=OptimizationModel(name="test", version="1.0"),
        confidence=0.9
    )
    
    state = {
        "timestamp": datetime.now(timezone.utc),
        "controller_health": "ONLINE",
        "phase_elapsed": 10 # Below minimum green!
    }
    
    return config, decision, state

def test_safety_rejects_min_green_violation():
    engine = SafetyEngine()
    config, decision, state = setup_test_data()
    
    # State has elapsed=10, min_green=15. Terminate should be rejected.
    result = engine.validate_action(decision, config, state)
    
    assert result.status == "REJECTED"
    assert result.reason_code == "MINIMUM_GREEN_NOT_REACHED"

def test_safety_rejects_stale_state():
    engine = SafetyEngine()
    config, decision, state = setup_test_data()
    
    # Make state 10 seconds old
    state["timestamp"] = datetime.now(timezone.utc) - timedelta(seconds=10)
    state["phase_elapsed"] = 20 # Passed min_green, but state is stale
    
    result = engine.validate_action(decision, config, state)
    
    assert result.status == "REJECTED"
    assert result.reason_code == "STALE_STATE"
    
def test_safety_approves_valid_action():
    engine = SafetyEngine()
    config, decision, state = setup_test_data()
    
    # Valid state, valid elapsed
    state["phase_elapsed"] = 20
    
    result = engine.validate_action(decision, config, state)
    
    assert result.status == "APPROVED"
    assert result.reason_code is None
