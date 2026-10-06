from src.platform.hardening.security.zero_trust import ZeroTrustEnforcer, AccessRequest, AccessResult
from src.platform.hardening.validation.readiness_gates import ReadinessEngine, ReadinessGate
from src.platform.hardening.validation.ai_validation import AIValidator, AIValidationStage
from src.platform.hardening.resilience.chaos_engine import ChaosEngine, ChaosScenario, SystemState
from src.platform.hardening.resilience.disaster_recovery import DREngine
import pytest

def test_zero_trust():
    enforcer = ZeroTrustEnforcer()
    enforcer.require_policy("pol-traffic-control")
    
    req = AccessRequest(
        request_id="req-1",
        who="agent-ai",
        what_resource="intersection-42",
        why="optimize flow",
        where_from="10.0.0.5",
        under_policy="pol-traffic-control",
        risk_level="LOW"
    )
    
    assert enforcer.evaluate(req) == AccessResult.GRANTED
    
    # Missing policy
    req.under_policy = "pol-unknown"
    assert enforcer.evaluate(req) == AccessResult.DENIED
    
    # High risk needs challenge/approval
    req.under_policy = "pol-traffic-control"
    req.risk_level = "HIGH"
    assert enforcer.evaluate(req) == AccessResult.CHALLENGED

def test_readiness_gates():
    engine = ReadinessEngine()
    engine.start_release("rel-1.0")
    engine.pass_gate("rel-1.0", ReadinessGate.G0_DESIGN)
    engine.pass_gate("rel-1.0", ReadinessGate.G3_SECURITY)
    
    assert not engine.is_production_ready("rel-1.0")
    
    engine.pass_gate("rel-1.0", ReadinessGate.G10_PROD)
    assert engine.is_production_ready("rel-1.0")

def test_ai_validation():
    validator = AIValidator()
    validator.register_model("model-cv-1")
    
    # Cannot approve without safety checks
    with pytest.raises(ValueError):
        validator.advance_stage("model-cv-1", AIValidationStage.APPROVED)
        
    profile = validator.profiles["model-cv-1"]
    profile.safety_invariants_checked = True
    
    # Cannot approve without 24h shadow mode
    with pytest.raises(ValueError):
        validator.advance_stage("model-cv-1", AIValidationStage.APPROVED)
        
    profile.shadow_mode_duration_hrs = 48
    validator.advance_stage("model-cv-1", AIValidationStage.APPROVED)
    assert profile.stage == AIValidationStage.APPROVED

def test_chaos_engine():
    engine = ChaosEngine()
    
    # Without safety fallback, AI offline causes system offline
    res1 = engine.run_experiment("exp-1", ChaosScenario.AI_OFFLINE, {"has_safety_fallback": False})
    assert not res1.survived
    assert res1.final_state == SystemState.OFFLINE
    
    # With safety fallback, system gracefully degrades
    res2 = engine.run_experiment("exp-2", ChaosScenario.AI_OFFLINE, {"has_safety_fallback": True})
    assert res2.survived
    assert res2.state_during_chaos == SystemState.LIMITED
    assert res2.final_state == SystemState.FULL

def test_dr_engine():
    engine = DREngine()
    engine.start_drill("drill-1", target_rto=60)
    
    # Missed RTO
    res1 = engine.complete_drill("drill-1", actual_rto=120, data_verified=True)
    assert not res1.successful
    
    # Met RTO and verified data
    engine.start_drill("drill-2", target_rto=60)
    res2 = engine.complete_drill("drill-2", actual_rto=45, data_verified=True)
    assert res2.successful
