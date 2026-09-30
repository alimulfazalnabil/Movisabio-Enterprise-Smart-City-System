import pytest
from aitcs.application.digital_twin_v2x_engine import DigitalTwinV2XEngine, V2XBasicSafetyMessage

def test_v2x_bsm_ingestion():
    engine = DigitalTwinV2XEngine()
    bsm = V2XBasicSafetyMessage(
        vehicle_id="V2X-VEH-01",
        latitude=23.8103,
        longitude=90.4125,
        speed_ms=14.2,
        heading_degrees=90.0,
        acceleration_mps2=0.5,
        intersection_id="INT-001"
    )
    success = engine.ingest_v2x_bsm(bsm)
    assert success is True
    assert len(engine.v2x_messages_buffer) == 1

def test_simulation_sync():
    engine = DigitalTwinV2XEngine()
    state = engine.sync_simulation_step("CARLA")
    assert state.simulation_engine == "CARLA"
    assert state.simulation_step == 1
    assert state.synchronization_status == "SYNCHRONIZED_ACTIVE"
