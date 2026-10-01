import pytest
from src.services.parking.models.schemas import CurbSegment, CurbStatus
from src.services.parking.engine.curb import CurbActivityEngine

def create_base_curb() -> CurbSegment:
    return CurbSegment(
        curb_id="C-001",
        road_id="R-001",
        permitted_use=["BUS_STOP"],
        capacity=2,
        restrictions=[],
        status=CurbStatus.ACTIVE
    )

def test_curb_engine_detects_double_parking():
    engine = CurbActivityEngine()
    curb = create_base_curb()
    
    track_data = {
        'speed': 0.0,
        'duration_stopped': 45,
        'within_curb_polygon': False,
        'in_travel_lane': True,
        'vehicle_type': 'CAR'
    }
    
    result = engine.evaluate_stop(curb, track_data)
    
    assert result is not None
    assert result['type'] == "DOUBLE_PARKING_CANDIDATE"

def test_curb_engine_detects_illegal_bus_stop_parking():
    engine = CurbActivityEngine()
    curb = create_base_curb()
    
    track_data = {
        'speed': 0.0,
        'duration_stopped': 20,
        'within_curb_polygon': True,
        'in_travel_lane': False,
        'vehicle_type': 'CAR' # Not a bus!
    }
    
    result = engine.evaluate_stop(curb, track_data)
    
    assert result is not None
    assert result['type'] == "ILLEGAL_STOPPING_CANDIDATE"

def test_curb_engine_ignores_legal_bus_stop():
    engine = CurbActivityEngine()
    curb = create_base_curb()
    
    track_data = {
        'speed': 0.0,
        'duration_stopped': 20,
        'within_curb_polygon': True,
        'in_travel_lane': False,
        'vehicle_type': 'BUS' # Legitimate user
    }
    
    result = engine.evaluate_stop(curb, track_data)
    
    assert result is None
