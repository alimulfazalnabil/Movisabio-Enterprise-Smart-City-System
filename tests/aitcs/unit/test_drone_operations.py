import pytest
from aitcs.application.drone_operations_engine import DroneOperationsEngine

def test_drone_dispatch_and_fleet():
    engine = DroneOperationsEngine()
    fleet = engine.get_fleet_telemetry()
    assert len(fleet) == 3

    mission = engine.dispatch_reconnaissance_drone("INT-001", "INCIDENT_RECONNAISSANCE")
    assert mission is not None
    assert mission.target_intersection_id == "INT-001"
    assert "rtsp://" in mission.rtsp_stream_url
