import pytest
from datetime import datetime, timezone
from src.services.network.models.schemas import RoadSegment
from src.services.network.engine.spillback import SpillbackPredictor

def test_spillback_prediction():
    predictor = SpillbackPredictor()
    
    # Storage is 200m, queue is 150m, growing at 1m/s
    seg1 = RoadSegment(
        segment_id="S1", source_intersection_id="I1", target_intersection_id="I2",
        length_meters=200, capacity_vph=1000, current_flow=800, current_speed=5.0,
        queue_length_meters=150.0, timestamp=datetime.now(timezone.utc)
    )
    
    event = predictor.evaluate_segment(seg1, queue_growth_mps=1.0)
    
    assert event is not None
    # 50m remaining / 1m/s = 50 seconds
    assert event.estimated_time_to_spillback_sec == pytest.approx(50.0)
    assert event.affected_upstream_intersection == "I1"
    
    # Storage 200m, queue 50m, shrinking
    seg2 = RoadSegment(
        segment_id="S1", source_intersection_id="I1", target_intersection_id="I2",
        length_meters=200, capacity_vph=1000, current_flow=800, current_speed=5.0,
        queue_length_meters=50.0, timestamp=datetime.now(timezone.utc)
    )
    assert predictor.evaluate_segment(seg2, queue_growth_mps=-0.5) is None
