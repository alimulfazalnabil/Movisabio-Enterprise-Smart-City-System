
import pytest
from aitcs.application.state_estimation import TrafficStateEstimationService
from aitcs.application.prediction_engine import TrafficPredictionEngine
from aitcs.application.decision_engine import AIDecisionEngine
from aitcs.application.safety_engine import SafetyValidationEngine
import numpy as np

def test_closed_loop_pipeline():
    # 1. State Estimation
    est_service = TrafficStateEstimationService()
    state = est_service.estimate_state("INT-001", {"vehicle_count": 45, "queue_length_meters": 80.0, "average_speed_kmh": 20.0})
    
    # 2. Prediction
    pred_engine = TrafficPredictionEngine()
    history = np.random.randn(10, 5)
    predictions = pred_engine.predict_future_states("INT-001", history)
    
    # 3. Decision
    dec_engine = AIDecisionEngine()
    decision = dec_engine.compute_signal_decision("INT-001", state, predictions)
    
    # 4. Safety Validation
    safety_engine = SafetyValidationEngine()
    sanitized = safety_engine.validate_and_sanitize(
        "INT-001", decision.selected_phase, decision.green_duration_seconds,
        decision.yellow_duration_seconds, decision.all_red_duration_seconds
    )
    
    assert sanitized.intersection_id == "INT-001"
    assert sanitized.green_duration_seconds >= 7
