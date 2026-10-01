import pytest
from datetime import datetime, timezone, timedelta
from src.services.parking.models.schemas import ParkingSpace, SpaceType, OccupancyStatus
from src.services.parking.engine.occupancy import ParkingOccupancyEngine, SensorObservation

def create_base_space() -> ParkingSpace:
    return ParkingSpace(
        space_id="P-001",
        tenant_id="T1",
        site_id="S1",
        zone_id="Z1",
        space_type=SpaceType.ON_STREET,
        status=OccupancyStatus.UNKNOWN,
        updated_at=datetime.now(timezone.utc)
    )

def test_occupancy_fusion_selects_highest_confidence():
    engine = ParkingOccupancyEngine()
    space = create_base_space()
    
    # Camera says occupied with 0.9 confidence
    cam_obs = SensorObservation("CAM-1", OccupancyStatus.OCCUPIED, 0.9, datetime.now(timezone.utc))
    # Sensor says vacant with 0.6 confidence
    sens_obs = SensorObservation("SENS-1", OccupancyStatus.VACANT, 0.6, datetime.now(timezone.utc))
    
    result = engine.fuse_occupancy(space, [cam_obs, sens_obs])
    
    assert result.status == OccupancyStatus.OCCUPIED
    assert result.occupancy_confidence == 0.9

def test_occupancy_fusion_ignores_stale_data():
    engine = ParkingOccupancyEngine()
    space = create_base_space()
    
    # Old camera observation
    old_time = datetime.now(timezone.utc) - timedelta(minutes=10)
    cam_obs = SensorObservation("CAM-1", OccupancyStatus.OCCUPIED, 0.99, old_time)
    
    result = engine.fuse_occupancy(space, [cam_obs])
    
    # Should revert to unknown because data is stale
    assert result.status == OccupancyStatus.UNKNOWN
    assert result.occupancy_confidence == 0.0

def test_occupancy_fusion_handles_no_observations():
    engine = ParkingOccupancyEngine()
    space = create_base_space()
    space.status = OccupancyStatus.OCCUPIED
    space.occupancy_confidence = 0.9
    
    result = engine.fuse_occupancy(space, [])
    
    # Reverts to UNKNOWN when stream drops
    assert result.status == OccupancyStatus.UNKNOWN
    assert result.occupancy_confidence == 0.0
