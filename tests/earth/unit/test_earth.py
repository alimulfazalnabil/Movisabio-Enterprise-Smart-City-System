from src.services.earth.models.schemas import GroundwaterObservation, GeologicalHazardObservation
from src.services.earth.engine.groundwater import GroundwaterEngine
from src.services.earth.engine.geological_hazard import GeologicalHazardEngine

def test_groundwater_risk():
    engine = GroundwaterEngine()
    
    # Stable
    obs_stable = [
        GroundwaterObservation(observation_id="1", aquifer_id="AQ1", well_id="W1", water_level_m=10.0, extraction_rate_m3_day=500, salinity=0.5),
        GroundwaterObservation(observation_id="2", aquifer_id="AQ1", well_id="W1", water_level_m=10.0, extraction_rate_m3_day=500, salinity=0.5)
    ]
    res_stable = engine.evaluate_aquifer_risk("AQ1", obs_stable)
    assert res_stable.state == "NORMAL"
    assert res_stable.trend == "STABLE"
    
    # Declining + Salinity
    obs_critical = [
        GroundwaterObservation(observation_id="1", aquifer_id="AQ1", well_id="W1", water_level_m=10.0, extraction_rate_m3_day=500, salinity=0.5),
        GroundwaterObservation(observation_id="2", aquifer_id="AQ1", well_id="W1", water_level_m=5.0, extraction_rate_m3_day=1500, salinity=2.0)
    ]
    res_crit = engine.evaluate_aquifer_risk("AQ1", obs_critical)
    assert res_crit.state == "CRITICAL"
    assert res_crit.trend == "DECLINING"

def test_geological_hazard():
    engine = GeologicalHazardEngine()
    
    obs = GeologicalHazardObservation(
        observation_id="OBS-1",
        zone_id="ZONE-A",
        hazard_type="LANDSLIDE",
        severity="HIGH",
        confidence=0.9
    )
    
    res = engine.detect_hazard_risk(obs, exposed_assets=["ROAD-1", "BRIDGE-2"])
    assert res.risk_level == "CRITICAL"
    assert "ROAD-1" in res.exposed_infrastructure
