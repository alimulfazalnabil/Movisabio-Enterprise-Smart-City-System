import pytest
from aitcs.application.smart_city_integrations_engine import SmartCityIntegrationsEngine

def test_smart_city_integrations():
    engine = SmartCityIntegrationsEngine()
    utility = engine.monitor_utility_grid("GRID-SUB-01")
    assert utility.station_id == "GRID-SUB-01"
    assert utility.status == "STABLE"

    report = engine.submit_citizen_report("POTHOLE", "Main Street pothole near intersection", 23.8103, 90.4125)
    assert report.category == "POTHOLE"
    assert report.status == "RECEIVED"
