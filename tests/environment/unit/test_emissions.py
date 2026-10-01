import pytest
from src.services.environment.engine.emissions import EmissionEstimator

def test_emission_estimation_for_free_flow():
    engine = EmissionEstimator()
    traffic_state = {
        "corridor_id": "C-1",
        "average_speed_kmh": 60,
        "idle_time_pct": 5,
        "stop_events_per_km": 0.5
    }
    
    result = engine.estimate_corridor_emissions(traffic_state)
    
    assert result["estimated_emission_level"] == "NORMAL"
    assert result["stop_and_go_index"] < 10

def test_emission_estimation_for_severe_stop_and_go():
    engine = EmissionEstimator()
    traffic_state = {
        "corridor_id": "C-2",
        "average_speed_kmh": 10,
        "idle_time_pct": 40,
        "stop_events_per_km": 8.0
    }
    
    result = engine.estimate_corridor_emissions(traffic_state)
    
    assert result["estimated_emission_level"] == "CRITICAL"
    assert result["stop_and_go_index"] > 20
