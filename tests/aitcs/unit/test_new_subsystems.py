import pytest
from aitcs.application.cv_anpr_engine import ComputerVisionANPREngine
from aitcs.application.environmental_weather_engine import EnvironmentalWeatherEngine
from aitcs.application.incident_emergency_engine import IncidentEmergencyEngine
from aitcs.infrastructure.spatial_repository import PostGISSpatialRepository

def test_cv_anpr_engine():
    engine = ComputerVisionANPREngine(blacklist_db=["DAH-9941"])
    telemetry = {
        "vehicle_count": 15,
        "pedestrian_count": 4,
        "emergency_vehicle_detected": True,
        "plates": [{"plate": "DAH-9941", "confidence": 0.98, "vehicle_type": "SUV"}]
    }
    result = engine.process_frame_telemetry("INT-001", telemetry)
    assert result.intersection_id == "INT-001"
    assert result.emergency_vehicle_detected is True
    assert len(result.detected_plates) == 1
    assert result.detected_plates[0].is_blacklisted is True

def test_environmental_weather_engine():
    engine = EnvironmentalWeatherEngine()
    metrics = engine.compute_environmental_impact("INT-001", 50, 15.0, weather_condition="RAIN")
    assert metrics.weather_condition == "RAIN"
    assert metrics.timing_multiplier == 1.25
    assert metrics.co2_estimation_kg_h > 0.0

def test_incident_emergency_engine():
    engine = IncidentEmergencyEngine()
    incidents = engine.detect_incidents("INT-001", {"wrong_way_detected": True, "sudden_stoppage_count": 4})
    assert len(incidents) == 2
    assert incidents[0].incident_type == "WRONG_WAY"
    assert incidents[1].incident_type == "ACCIDENT"

def test_postgis_spatial_repository():
    repo = PostGISSpatialRepository()
    coords = repo.get_intersection_location("INT-001")
    assert coords == (23.8103, 90.4125)
    inside = repo.check_geofence(23.8100, 90.4100, "downtown_zone")
    assert isinstance(inside, bool)
