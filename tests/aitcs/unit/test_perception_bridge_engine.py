from aitcs.application.perception_bridge_engine import PerceptionBridgeEngine


def test_perception_engine_flags_lane_departure_as_critical():
    engine = PerceptionBridgeEngine()
    record = engine.process_perception_frame(
        "INT-001", "VEH-001", True, 35.0, 0.2, 4
    )

    evaluation = engine.evaluate_safety_threshold(record)

    assert evaluation["critical_alert"] is True
    assert evaluation["recommended_action"] == "NORMAL_MONITORING"


def test_perception_engine_recommends_emergency_braking_for_high_risk():
    engine = PerceptionBridgeEngine()
    record = engine.process_perception_frame(
        "INT-001", "VEH-002", False, 35.0, 0.9, 4
    )

    evaluation = engine.evaluate_safety_threshold(record)

    assert evaluation["critical_alert"] is True
    assert evaluation["recommended_action"] == "EMERGENCY_BRAKING_RECOMMENDED"


def test_perception_engine_keeps_only_latest_two_thousand_records():
    engine = PerceptionBridgeEngine()
    for index in range(2001):
        engine.process_perception_frame(
            "INT-001", f"VEH-{index}", False, 35.0, 0.1, 1
        )

    assert len(engine.telemetry_history) == 2000
    assert engine.telemetry_history[0].vehicle_id == "VEH-1"