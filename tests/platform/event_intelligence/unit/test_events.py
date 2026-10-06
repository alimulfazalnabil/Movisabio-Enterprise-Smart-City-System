from datetime import datetime, timezone, timedelta
from src.platform.event_intelligence.cep.engine import CEPEngine, CEPPattern, EventEnvelope
from src.platform.anomaly.ensembles.detector import AnomalyEnsemble
from src.platform.situation_awareness.engine.situation import SituationEngine, SituationStatus
from src.platform.early_warning.forecast import EarlyWarningEngine, EventForecast, WarningLevel

def test_cep_engine():
    engine = CEPEngine()
    pattern = CEPPattern(
        pattern_id="congestion_pattern",
        target_event_type="traffic.queue_increased",
        conditions=[],
        time_window_seconds=300
    )
    engine.register_pattern(pattern)
    
    event = EventEnvelope(
        event_id="evt-1",
        event_type="traffic.queue_increased",
        tenant_id="t1",
        source_type="sensor",
        source_id="s1",
        event_time=datetime.now(timezone.utc),
        classification="OPERATIONAL",
        payload={"queue_length": 50}
    )
    
    detected = engine.process_event(event)
    assert len(detected) == 1
    assert detected[0]["pattern_id"] == "congestion_pattern"

def test_anomaly_ensemble():
    ensemble = AnomalyEnsemble()
    
    # Normal condition
    assert ensemble.detect_anomalies("road-1", current_value=100, context={"historical_average": 100, "is_holiday": False}) is None
    
    # Anomaly condition (value is 1.6x baseline)
    anomaly = ensemble.detect_anomalies("road-1", current_value=160, context={"historical_average": 100, "is_holiday": False})
    assert anomaly is not None
    assert anomaly.score == 0.85

def test_situation_engine():
    engine = SituationEngine()
    
    events = [
        {"event_id": "e1", "domain": "weather", "type": "heavy_rain"},
        {"event_id": "e2", "domain": "traffic", "type": "speed_drop"}
    ]
    
    situation = engine.evaluate_correlation(events)
    assert situation is not None
    assert situation.type == "WEATHER_TRAFFIC_DISRUPTION"
    assert situation.status == SituationStatus.ACTIVE
    assert len(situation.evidence_events) == 2

def test_early_warning():
    engine = EarlyWarningEngine()
    
    now = datetime.now(timezone.utc)
    forecast_critical = EventForecast(
        event_type="FLOOD",
        expected_window_start=now,
        expected_window_end=now + timedelta(hours=2),
        location="district-9",
        probability=0.85,
        potential_severity="CRITICAL"
    )
    
    warning = engine.evaluate_forecast(forecast_critical)
    assert warning is not None
    assert warning["level"] == WarningLevel.WARNING
    
    forecast_low = EventForecast(
        event_type="QUEUE_SPILLOVER",
        expected_window_start=now,
        expected_window_end=now + timedelta(hours=1),
        location="corridor-1",
        probability=0.30,
        potential_severity="LOW"
    )
    
    assert engine.evaluate_forecast(forecast_low) is None
