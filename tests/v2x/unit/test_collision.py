import pytest
from datetime import datetime, timezone
from src.services.v2x.models.schemas import CooperativeObject
from src.services.v2x.engine.collision import CollisionRiskEngine

def test_collision_risk_detection():
    engine = CollisionRiskEngine()
    
    # 55.5 meters apart
    obj_a = CooperativeObject(
        object_id="A1", object_type="VEHICLE", position={"latitude": 20.0, "longitude": 0.0},
        velocity_mps=15.0, heading_deg=0.0, sources=[], confidence=1.0, state="MOVING", last_updated=datetime.now(timezone.utc)
    )
    
    # 1 degree of latitude is ~111,000 meters. 
    # Let's put B exactly 55.5 meters away (55.5 / 111000 = 0.0005)
    obj_b = CooperativeObject(
        object_id="B1", object_type="VEHICLE", position={"latitude": 20.0005, "longitude": 0.0},
        velocity_mps=15.0, heading_deg=180.0, sources=[], confidence=1.0, state="MOVING", last_updated=datetime.now(timezone.utc)
    )
    
    risk = engine.evaluate_risk(obj_a, obj_b)
    
    assert risk is not None
    # Rel speed is 30m/s. Distance is 55.5m. TTC = ~1.85 seconds, which is < 5.0
    assert risk.time_to_collision_sec < 5.0
