import pytest
from src.services.mobile.models.schemas import MobileAsset, MissionPackage, GeofenceZone
from src.services.mobile.engine.fleet import FleetOptimizationEngine

def test_fleet_assignment():
    engine = FleetOptimizationEngine()
    
    asset1 = MobileAsset(asset_id="A1", tenant_id="T1", asset_type="DRONE", status="AVAILABLE", capabilities=[], battery_state=25.0, connectivity_state="ONLINE")
    asset2 = MobileAsset(asset_id="A2", tenant_id="T1", asset_type="DRONE", status="ON_MISSION", capabilities=[], battery_state=90.0, connectivity_state="ONLINE")
    asset3 = MobileAsset(asset_id="A3", tenant_id="T1", asset_type="DRONE", status="AVAILABLE", capabilities=[], battery_state=85.0, connectivity_state="ONLINE")
    
    mission = MissionPackage(
        mission_id="M1", asset_id="", mission_type="INSPECTION",
        priority="P1", status="PLANNING", waypoints=[],
        geofence=GeofenceZone(zone_id="Z1", zone_type="ALLOWED", geometry={}), 
        safety_policy={}, abort_conditions=[], authorization_required=False
    )
    
    best_asset_id = engine.assign_mission(mission, [asset1, asset2, asset3])
    
    # A1 has low battery (<30), A2 is ON_MISSION. A3 is the only valid choice.
    assert best_asset_id == "A3"
