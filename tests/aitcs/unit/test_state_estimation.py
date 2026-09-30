
import pytest
from aitcs.application.state_estimation import TrafficStateEstimationService
from aitcs.domain.value_objects import LevelOfService

def test_state_estimation_optimal():
    service = TrafficStateEstimationService()
    telemetry = {
        "vehicle_count": 10,
        "pedestrian_count": 2,
        "occupancy_percentage": 15.0,
        "queue_length_meters": 10.0,
        "average_speed_kmh": 45.0,
        "max_speed_kmh": 50.0
    }
    state = service.estimate_state("INT-001", telemetry)
    assert state.intersection_id == "INT-001"
    assert state.level_of_service == LevelOfService.A
    assert state.congestion_index < 0.3
