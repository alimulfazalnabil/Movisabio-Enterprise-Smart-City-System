import pytest
from datetime import datetime, timezone
from backend.app.traffic.perception import Track
from backend.app.traffic.lane_logic import LaneConfig, LaneManager
from backend.app.traffic.speed import SpeedEstimator
from backend.app.traffic.state import TrafficStateAggregator

@pytest.fixture
def mock_lanes():
    return [
        LaneConfig(
            lane_id="N1",
            direction="Northbound",
            movement="Straight",
            polygon=[[0, 0], [10, 0], [10, 10], [0, 10]],
            speed_limit=50.0,
            crossing_line=[[0, 5], [10, 5]]
        )
    ]

def test_lane_assignment(mock_lanes):
    manager = LaneManager(mock_lanes)
    t = Track("trk_1", "car", [2, 2, 8, 8], datetime.now(timezone.utc))
    assigned = manager.assign_lane(t)
    assert assigned == "N1"

def test_speed_estimation():
    est = SpeedEstimator(calibration_matrix=None) # Identity matrix
    t = Track("trk_1", "car", [0, 0, 2, 2], datetime.now(timezone.utc))
    # mock second point 1 second later
    import time
    time.sleep(0.1) # small delay for testing
    t.update([10, 10, 12, 12], datetime.now(timezone.utc))
    
    speed = est.estimate_speed(t)
    assert speed > 0

def test_traffic_state_aggregation(mock_lanes):
    manager = LaneManager(mock_lanes)
    est = SpeedEstimator(calibration_matrix=None)
    agg = TrafficStateAggregator(manager, est)
    
    t = Track("trk_1", "car", [2, 2, 8, 8], datetime.now(timezone.utc))
    
    state = agg.aggregate("INT-001", [t])
    assert state["vehicle_count"] == 1
    assert state["congestion_level"] == "LIGHT"
    assert state["lane_states"]["N1"]["instantaneous_count"] == 1
