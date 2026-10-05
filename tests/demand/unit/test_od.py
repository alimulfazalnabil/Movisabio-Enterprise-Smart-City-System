import pytest
from datetime import datetime, timezone
from src.services.demand.models.schemas import MobilityDemand
from src.services.demand.engine.od import ODEstimator

def test_od_matrix_generation():
    estimator = ODEstimator()
    
    demands = [
        MobilityDemand(origin_zone="Z1", destination_zone="Z2", time_window_start=datetime.now(timezone.utc), time_window_end=datetime.now(timezone.utc), mode="CAR", trip_purpose="COMMUTE", volume_estimate=100, confidence=0.9),
        MobilityDemand(origin_zone="Z1", destination_zone="Z2", time_window_start=datetime.now(timezone.utc), time_window_end=datetime.now(timezone.utc), mode="BUS", trip_purpose="COMMUTE", volume_estimate=50, confidence=0.8),
        MobilityDemand(origin_zone="Z2", destination_zone="Z1", time_window_start=datetime.now(timezone.utc), time_window_end=datetime.now(timezone.utc), mode="CAR", trip_purpose="COMMUTE", volume_estimate=75, confidence=0.9)
    ]
    
    matrix = estimator.generate_matrix(demands, zones=["Z1", "Z2", "Z3"])
    
    assert matrix.flow_matrix["Z1"]["Z2"] == 150 # 100 + 50
    assert matrix.flow_matrix["Z2"]["Z1"] == 75
    assert matrix.flow_matrix["Z1"]["Z3"] == 0
