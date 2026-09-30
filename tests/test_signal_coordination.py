import pytest
from src.network.topology_loader import TopologyLoader
from src.optimization.corridor_optimizer import CorridorOptimizer

@pytest.fixture
def sample_topology():
    data = {
        "intersections": [{"id": "INT-001"}, {"id": "INT-002"}, {"id": "INT-003"}],
        "corridors": [
            {"upstream": "INT-001", "downstream": "INT-002", "distance_m": 450.0},
            {"upstream": "INT-002", "downstream": "INT-003", "distance_m": 620.0}
        ]
    }
    return TopologyLoader.load_from_dict(data)

def test_green_wave_offsets(sample_topology):
    optimizer = CorridorOptimizer(sample_topology)
    
    # 15 m/s (~54 km/h)
    offsets = optimizer.calculate_offsets(15.0)
    
    assert offsets["INT-001"] == 0.0
    assert offsets["INT-002"] == 450.0 / 15.0  # 30s
    assert offsets["INT-003"] == (450.0 + 620.0) / 15.0 # 71.33s

def test_spillback_detection(sample_topology):
    optimizer = CorridorOptimizer(sample_topology)
    
    # Distance is 450m. 80% is 360m. 360 / 7m per car = ~51 cars.
    # 52 cars should trigger it.
    is_risk = optimizer.detect_spillback_risk("INT-001", "INT-002", 52)
    assert is_risk == True
    
    # 10 cars should be safe.
    is_safe = optimizer.detect_spillback_risk("INT-001", "INT-002", 10)
    assert is_safe == False
