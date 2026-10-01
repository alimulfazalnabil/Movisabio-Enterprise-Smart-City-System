import pytest
from src.services.digital_twin.engine.evaluation import InterventionEvaluationEngine

def test_intervention_evaluation():
    engine = InterventionEvaluationEngine()
    
    baseline = {"travel_time_sec": 600.0, "emissions_kg": 50.0}
    actual = {"travel_time_sec": 400.0, "emissions_kg": 40.0}
    
    eval_result = engine.evaluate("INV-1", baseline, actual)
    
    # 600 - 400 = +200 improvement
    assert eval_result.estimated_effects["travel_time_sec"] == 200.0
    # 50 - 40 = +10 improvement
    assert eval_result.estimated_effects["emissions_kg"] == 10.0
    assert "travel_time_sec" in eval_result.metrics_compared
    assert eval_result.uncertainty["travel_time_sec"] == 20.0 # 10% of 200
