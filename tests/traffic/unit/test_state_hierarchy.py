import pytest
from datetime import datetime
from src.services.traffic.state.models import (
    LaneTrafficState, ApproachState, IntersectionState, TrafficLevel, StateDataQuality
)

def test_hierarchy_parsing():
    lane = LaneTrafficState(
        lane_id="N1",
        timestamp=datetime.utcnow(),
        vehicles=10,
        flow_veh_per_hour=100.0,
        average_speed_kmh=45.0,
        density_veh_per_km=10.0,
        queue_length_m=5.0,
        queue_vehicles=1,
        occupancy_ratio=0.1,
        delay_seconds=2.0,
        data_quality=1.0
    )
    
    approach = ApproachState(
        approach_id="NORTH",
        vehicle_count=10,
        average_speed_kmh=45.0,
        queue_length_m=5.0,
        flow_veh_per_hour=100.0,
        density_veh_per_km=10.0,
        delay_seconds=2.0,
        lanes=[lane]
    )
    
    intersection = IntersectionState(
        intersection_id="INT_01",
        timestamp=datetime.utcnow(),
        state=TrafficLevel.FREE_FLOW,
        congestion_index=0.1,
        approaches={"NORTH": approach},
        data_quality=StateDataQuality(
            overall=1.0, camera=1.0, tracking=1.0, calibration=1.0, signal=1.0, freshness=1.0
        )
    )
    
    assert intersection.approaches["NORTH"].lanes[0].lane_id == "N1"
