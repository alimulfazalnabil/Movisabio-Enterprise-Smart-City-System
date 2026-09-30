import pytest
from aitcs.application.pedestrian_intelligence_engine import PedestrianIntelligenceEngine
from aitcs.application.mlops_xai_engine import MLOpsXAIEngine

def test_pedestrian_intelligence():
    engine = PedestrianIntelligenceEngine()
    state = engine.calculate_crossing_timing("INT-001", waiting_count=20, elderly_count=2, school_mode=True)
    assert state.recommended_crossing_duration_seconds > 25
    assert state.school_crossing_active is True

def test_mlops_xai_engine():
    engine = MLOpsXAIEngine()
    explanation = engine.explain_decision("DEC-991", "v3.2.0", {"queue_length": 45.0, "density": 0.8, "speed": 12.5})
    assert explanation.confidence_score > 0.9
    assert "queue_length" in explanation.feature_importances
    assert explanation.drift_detected is False
