import pytest
from datetime import datetime, timezone
from src.services.agriculture.models.schemas import Livestock, GeoPoint, FenceState
from src.services.agriculture.engine.livestock import VirtualFenceEngine

def create_base_animal(state: FenceState) -> Livestock:
    return Livestock(
        animal_id="COW-1",
        farm_id="FARM-1",
        species="CATTLE",
        breed="ANGUS",
        location=GeoPoint(lat=0.0, lon=0.0),
        health_state="NORMAL",
        battery_state=0.9,
        fence_zone="GRAZING_ZONE",
        fence_state=state,
        timestamp=datetime.now(timezone.utc)
    )

def test_livestock_approaches_boundary():
    engine = VirtualFenceEngine()
    animal = create_base_animal(FenceState.NORMAL)
    
    # 40m away, moving towards
    result = engine.evaluate_position(animal, distance_to_boundary_m=40.0, moving_towards_boundary=True)
    
    assert result.fence_state == FenceState.APPROACHING_BOUNDARY

def test_livestock_warning():
    engine = VirtualFenceEngine()
    animal = create_base_animal(FenceState.APPROACHING_BOUNDARY)
    
    # 10m away, moving towards
    result = engine.evaluate_position(animal, distance_to_boundary_m=10.0, moving_towards_boundary=True)
    
    assert result.fence_state == FenceState.BOUNDARY_WARNING

def test_livestock_breach_candidate():
    engine = VirtualFenceEngine()
    animal = create_base_animal(FenceState.BOUNDARY_WARNING)
    
    # Crossed the line
    result = engine.evaluate_position(animal, distance_to_boundary_m=-5.0, moving_towards_boundary=True)
    
    assert result.fence_state == FenceState.BOUNDARY_BREACH_CANDIDATE

def test_livestock_returns_to_normal():
    engine = VirtualFenceEngine()
    animal = create_base_animal(FenceState.BOUNDARY_WARNING)
    
    # Stopped moving towards boundary, walked back to 35m
    result = engine.evaluate_position(animal, distance_to_boundary_m=35.0, moving_towards_boundary=False)
    
    assert result.fence_state == FenceState.NORMAL
