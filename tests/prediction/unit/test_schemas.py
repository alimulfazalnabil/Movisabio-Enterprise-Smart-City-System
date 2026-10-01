import pytest
from datetime import datetime, timezone
from src.services.prediction.features.models import TrafficFeatureVector
from src.services.prediction.models.schema import TrafficPrediction

def test_feature_vector_instantiation():
    fv = TrafficFeatureVector(
        timestamp=datetime.now(timezone.utc),
        intersection_id="INT-001",
        volume=120.0,
        speed=45.0,
        density=10.0,
        queue_length=0.0,
        occupancy=0.2,
        delay=0.0,
        congestion_index=0.1,
        signal_phase="NORTH_GREEN",
        phase_elapsed=10.0,
        incident_indicator=0.0,
        weather_features={"rain": 0.0},
        data_quality=1.0
    )
    assert fv.intersection_id == "INT-001"
    assert fv.congestion_index == 0.1

def test_prediction_instantiation():
    pred = TrafficPrediction(
        prediction_id="pred-123",
        tenant_id="tenant-1",
        intersection_id="INT-001",
        generated_at=datetime.now(timezone.utc),
        target_time=datetime.now(timezone.utc),
        horizon_seconds=300,
        metric="queue_length",
        predicted_value=120.5,
        lower_bound=100.0,
        upper_bound=140.0,
        confidence=0.9,
        model_id="lstm-v1",
        model_version="1.0.0",
        feature_version="f-v1",
        data_quality=0.95
    )
    assert pred.metric == "queue_length"
    assert pred.horizon_seconds == 300
