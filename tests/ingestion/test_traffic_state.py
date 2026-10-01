import pytest
from datetime import datetime
from src.packages.domain.traffic_state import IntersectionTrafficState, IntersectionMetrics, TrafficDataQuality

def test_intersection_traffic_state_creation():
    state = IntersectionTrafficState(
        intersection_id="int_01",
        timestamp=datetime.utcnow(),
        traffic=IntersectionMetrics(
            vehicle_count=184,
            average_speed_kmh=23.7,
            density=0.71,
            queue_length=284,
            congestion_index=0.68
        ),
        data_quality=TrafficDataQuality(score=0.93)
    )
    
    assert state.traffic.vehicle_count == 184
    assert state.data_quality.score == 0.93
    assert len(state.lanes) == 0
