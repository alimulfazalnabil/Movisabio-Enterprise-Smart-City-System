import pytest
from src.services.traffic.state.congestion import CongestionModel
from src.services.traffic.state.models import TrafficLevel

def test_congestion_index_calculation():
    model = CongestionModel()
    
    ci = model.calculate_index(
        speed_degradation=0.5,
        normalized_queue=0.5,
        density=0.5,
        occupancy=0.5,
        delay=0.5
    )
    
    assert ci == 0.5
    assert model.classify_state(ci) == TrafficLevel.MODERATE

def test_severe_congestion():
    model = CongestionModel()
    
    ci = model.calculate_index(1.0, 1.0, 1.0, 1.0, 1.0)
    assert ci == 1.0
    assert model.classify_state(ci) == TrafficLevel.SEVERE
