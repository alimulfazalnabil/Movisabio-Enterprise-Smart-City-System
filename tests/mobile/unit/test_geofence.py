import pytest
from datetime import datetime, timezone
from src.services.mobile.models.schemas import GeofenceZone, AssetTelemetry
from src.services.mobile.engine.geofence import GeofenceEngine

def test_geofence_allowed_zone():
    engine = GeofenceEngine()
    
    zone = GeofenceZone(zone_id="Z1", zone_type="ALLOWED", geometry={})
    
    telemetry_inside = AssetTelemetry(
        asset_id="A1", timestamp=datetime.now(timezone.utc),
        latitude=22.0, longitude=90.0, speed=10, heading=0, battery=100, gps_quality="VALID"
    )
    assert engine.evaluate_position(telemetry_inside, zone) == "INSIDE_ALLOWED_ZONE"
    
    telemetry_warning = AssetTelemetry(
        asset_id="A1", timestamp=datetime.now(timezone.utc),
        latitude=24.5, longitude=90.0, speed=10, heading=0, battery=100, gps_quality="VALID"
    )
    assert engine.evaluate_position(telemetry_warning, zone) == "BOUNDARY_WARNING"
    
    telemetry_breach = AssetTelemetry(
        asset_id="A1", timestamp=datetime.now(timezone.utc),
        latitude=30.0, longitude=90.0, speed=10, heading=0, battery=100, gps_quality="VALID"
    )
    assert engine.evaluate_position(telemetry_breach, zone) == "BREACH_DETECTED"
