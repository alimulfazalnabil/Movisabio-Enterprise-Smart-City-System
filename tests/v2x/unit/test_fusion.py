import pytest
from src.services.v2x.engine.fusion import CooperativePerceptionEngine

def test_sensor_fusion():
    engine = CooperativePerceptionEngine()
    
    observations = [
        {"source": "VEHICLE-1", "lat": 20.0, "lon": 90.0, "speed": 10.0},
        {"source": "CAMERA-4", "lat": 20.0001, "lon": 90.0, "speed": 10.2},
        {"source": "RSU-2", "lat": 19.9999, "lon": 90.0, "speed": 9.8}
    ]
    
    obj = engine.fuse_observations("OBJ-1", observations)
    
    assert obj.position["latitude"] == pytest.approx(20.0)
    assert obj.velocity_mps == pytest.approx(10.0)
    assert obj.confidence > 0.8 # Multiple sources increase confidence
    assert len(obj.sources) == 3
