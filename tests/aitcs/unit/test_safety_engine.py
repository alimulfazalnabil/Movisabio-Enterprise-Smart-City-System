
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
        active_conflicting_phases={3}
    )
    assert command.is_fallback_active is True
    assert command.approved_phase == 1
