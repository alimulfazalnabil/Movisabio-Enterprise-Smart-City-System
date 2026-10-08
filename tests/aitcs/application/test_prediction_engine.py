import numpy as np
import pytest

from aitcs.application.prediction_engine import FEATURE_ORDER, TrafficPredictionEngine


def test_prediction_baseline_is_deterministic_and_provenanced():
    history = np.array(
        [[20, 25, 30, 30, 0.25], [24, 30, 40, 28, 0.35]],
        dtype=np.float32,
    )
    engine = TrafficPredictionEngine()

    first = engine.predict_future_states("INT-001", history, correlation_id="c1")
    second = engine.predict_future_states("INT-001", history, correlation_id="c1")

    assert FEATURE_ORDER == (
        "vehicle_count",
        "occupancy_percentage",
        "queue_length_meters",
        "average_speed_kmh",
        "congestion_index",
    )
    assert first == second
    assert first[0].evidence_class == "PREDICTED_BASELINE"
    assert first[0].predicted_queue_length_meters == 40.0


def test_operational_ml_requires_checkpoint():
    engine = TrafficPredictionEngine()
    history = np.ones((4, 5), dtype=np.float32)

    with pytest.raises(RuntimeError, match="trained checkpoint"):
        engine.predict_future_states("INT-001", history, require_ml=True)


def test_prediction_rejects_invalid_shape():
    engine = TrafficPredictionEngine()
    with pytest.raises(ValueError):
        engine.predict_future_states("INT-001", np.ones((4, 4), dtype=np.float32))
