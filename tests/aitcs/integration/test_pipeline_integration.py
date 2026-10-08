import numpy as np

from aitcs.application.decision_engine import AIDecisionEngine
from aitcs.application.prediction_engine import TrafficPredictionEngine
from aitcs.application.safety_engine import SafetyValidationEngine
from aitcs.application.state_estimation import TrafficStateEstimationService


def test_closed_loop_pipeline_uses_explicit_prediction_provenance():
    est_service = TrafficStateEstimationService()
    state = est_service.estimate_state(
        "INT-001",
        {
            "vehicle_count": 45,
            "pedestrian_count": 3,
            "occupancy_percentage": 42.0,
            "queue_length_meters": 80.0,
            "average_speed_kmh": 20.0,
            "max_speed_kmh": 40.0,
            "turning_left_count": 10,
            "turning_right_count": 8,
            "straight_count": 27,
        },
    )

    # Deterministic baseline history: no random test data and no fake ML claim.
    history = np.array(
        [
            [40, 38, 70, 22, 0.55],
            [42, 40, 74, 21, 0.58],
            [45, 42, 80, 20, 0.61],
        ],
        dtype=np.float32,
    )

    pred_engine = TrafficPredictionEngine()
    predictions = pred_engine.predict_future_states(
        "INT-001", history, correlation_id="corr-test-001"
    )

    assert len(predictions) == 4
    assert all(p.evidence_class == "PREDICTED_BASELINE" for p in predictions)
    assert all(p.correlation_id == "corr-test-001" for p in predictions)

    dec_engine = AIDecisionEngine()
    decision = dec_engine.compute_signal_decision("INT-001", state, predictions)

    safety_engine = SafetyValidationEngine()
    sanitized = safety_engine.validate_and_sanitize(
        "INT-001",
        decision.selected_phase,
        decision.green_duration_seconds,
        decision.yellow_duration_seconds,
        decision.all_red_duration_seconds,
    )

    assert sanitized.intersection_id == "INT-001"
    assert sanitized.green_duration_seconds >= 7
