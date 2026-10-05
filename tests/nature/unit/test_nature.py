from src.services.nature.models.schemas import WildfireObservation, ForestChangeEvent
from src.services.nature.engine.biodiversity_indicator import BiodiversityEngine
from src.services.nature.engine.forest_change import ForestChangeEngine
from src.services.nature.engine.wildfire import WildfireRiskEngine

def test_biodiversity_health():
    engine = BiodiversityEngine()
    
    # Restoring
    ind_restore = engine.calculate_health(0.8, 0.7, 0.9, "ZONE-1")
    assert ind_restore.overall_health == "RESTORING"
    
    # Degraded
    ind_deg = engine.calculate_health(0.2, 0.3, 0.1, "ZONE-2")
    assert ind_deg.overall_health == "DEGRADED"
    
def test_forest_change():
    engine = ForestChangeEngine()
    
    ev_pending = ForestChangeEvent(
        event_id="EV-1",
        forest_id="FOR-1",
        change_type="CANOPY_LOSS_CANDIDATE",
        estimated_area_m2=5000,
        confidence=0.9,
        verification_status="PENDING"
    )
    
    assert engine.evaluate_change(ev_pending) == "VERIFICATION_REQUIRED"
    
    ev_verified = ForestChangeEvent(
        event_id="EV-1",
        forest_id="FOR-1",
        change_type="CANOPY_LOSS_CANDIDATE",
        estimated_area_m2=5000,
        confidence=0.9,
        verification_status="VERIFIED"
    )
    assert engine.evaluate_change(ev_verified) == "ACTION_REQUIRED"

def test_wildfire_risk():
    engine = WildfireRiskEngine()
    
    obs_extreme = WildfireObservation(
        observation_id="OBS-1",
        zone_id="ZONE-W",
        temperature_c=40.0,
        humidity_percent=10.0,
        wind_speed_kmh=45.0,
        fuel_load="EXTREME",
        smoke_detected=False
    )
    
    res = engine.evaluate_risk(obs_extreme)
    assert res.risk_level == "EXTREME"
    
    obs_smoke = WildfireObservation(
        observation_id="OBS-2",
        zone_id="ZONE-W",
        temperature_c=25.0,
        humidity_percent=50.0,
        wind_speed_kmh=10.0,
        fuel_load="LOW",
        smoke_detected=True
    )
    
    res_smoke = engine.evaluate_risk(obs_smoke)
    assert res_smoke.risk_level == "EXTREME"
    assert res_smoke.confidence > 0.9
