import pytest

from aitcs.application.safety_engine import SafetyValidationEngine


def test_safety_engine_conflict_fallback():
    engine = SafetyValidationEngine()
    command = engine.validate_and_sanitize(
        intersection_id="INT-001",
        requested_phase=1,
        requested_green=60,
        requested_yellow=4,
        requested_all_red=2,
        active_conflicting_phases={3},
    )
    assert command.is_fallback_active is True
    assert command.approved_phase == 1


def test_emergency_does_not_bypass_timing_bounds():
    engine = SafetyValidationEngine(max_green=90)
    command = engine.validate_and_sanitize(
        "INT-001", 1, 999, 1, 1, is_emergency=True
    )
    assert command.is_fallback_active is False
    assert command.green_duration_seconds == 90
    assert command.yellow_duration_seconds == 4
    assert command.all_red_duration_seconds == 2
    assert "Emergency" in command.override_reason


def test_unknown_phase_fails_safe():
    engine = SafetyValidationEngine()
    command = engine.validate_and_sanitize("INT-001", 99, 30, 4, 2)
    assert command.is_fallback_active is True


def test_invalid_timing_fails_safe():
    engine = SafetyValidationEngine()
    command = engine.validate_and_sanitize("INT-001", 1, 0, 4, 2)
    assert command.is_fallback_active is True
