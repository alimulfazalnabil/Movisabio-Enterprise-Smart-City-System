import pytest
from src.services.logistics.models.schemas import LoadingZone
from src.services.logistics.engine.curb import CurbManagementEngine

def test_curb_arrival_departure():
    engine = CurbManagementEngine()
    
    zone = LoadingZone(zone_id="LZ1", status="AVAILABLE", capacity=2, current_occupancy=1)
    
    # First arrival should succeed
    res1 = engine.process_arrival(zone)
    assert res1 == "ACCEPTED"
    assert zone.current_occupancy == 2
    assert zone.status == "OCCUPIED"
    
    # Second arrival should be rejected
    res2 = engine.process_arrival(zone)
    assert res2 == "REJECTED_FULL"
    
    # Departure should free up space
    engine.process_departure(zone)
    assert zone.current_occupancy == 1
    assert zone.status == "AVAILABLE"
