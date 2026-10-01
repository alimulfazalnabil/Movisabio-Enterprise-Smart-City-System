import pytest
from src.services.mobile.models.schemas import MissionPackage, GeofenceZone
from src.services.mobile.engine.mission import MissionManager

def test_mission_authorization_requires_human():
    manager = MissionManager()
    
    geofence = GeofenceZone(zone_id="Z1", zone_type="ALLOWED", geometry={})
    mission = MissionPackage(
        mission_id="M1", asset_id="A1", mission_type="INSPECTION",
        priority="P1", status="PENDING_AUTHORIZATION", waypoints=[],
        geofence=geofence, safety_policy={}, abort_conditions=[],
        authorization_required=True
    )
    
    # Fails without operator approval
    assert manager.authorize_mission(mission, operator_approved=False) is False
    assert mission.status == "PENDING_AUTHORIZATION"
    
    # Succeeds with operator approval
    assert manager.authorize_mission(mission, operator_approved=True) is True
    assert mission.status == "AUTHORIZED"

def test_mission_abort():
    manager = MissionManager()
    
    geofence = GeofenceZone(zone_id="Z1", zone_type="ALLOWED", geometry={})
    mission = MissionPackage(
        mission_id="M1", asset_id="A1", mission_type="INSPECTION",
        priority="P1", status="ACTIVE", waypoints=[],
        geofence=geofence, safety_policy={}, abort_conditions=[],
        authorization_required=False
    )
    
    assert manager.abort_mission(mission, reason="WEATHER_DEGRADED") is True
    assert mission.status == "ABORTED"
