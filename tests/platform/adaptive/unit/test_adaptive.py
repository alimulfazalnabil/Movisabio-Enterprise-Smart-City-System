from src.platform.adaptive.sensing.anomaly_engine import AnomalyEngine, Anomaly, AnomalyType
from src.platform.adaptive.planning.adaptive_planner import AdaptivePlanner, ExecutionPlan, PlanStatus
from src.platform.adaptive.resilience.stress_tester import StressTester, StressScenario, StressScenarioType
from src.platform.autonomous_operations.action_engine.action_ledger import ActionLedger, AutonomousAction, AutonomyLevel, ActionStatus
from datetime import datetime, timezone

def test_anomaly_engine():
    engine = AnomalyEngine()
    
    a1 = Anomaly(anomaly_id="a-1", type=AnomalyType.FINANCIAL, metric="cloud_cost", observed_value=1500, expected_value=1000, confidence=0.9)
    a2 = Anomaly(anomaly_id="a-2", type=AnomalyType.INFRASTRUCTURE, metric="gpu_demand", observed_value=100, expected_value=80, confidence=0.95)
    
    engine.detect_anomaly(a1)
    engine.detect_anomaly(a2)
    
    # Should have correlated into a situation
    assert "sit-ai-infra-risk" in engine.situations
    assert len(engine.situations["sit-ai-infra-risk"].anomalies) == 2

def test_adaptive_planner():
    planner = AdaptivePlanner()
    plan = ExecutionPlan(
        plan_id="plan-1",
        target_date=datetime.now(timezone.utc),
        budget=10000,
        resources_needed=5
    )
    planner.register_plan(plan)
    
    adapted = planner.adapt_plan("plan-1", "sit-ai-infra-risk", budget_change=2000, schedule_delay_days=14)
    
    assert adapted.status == PlanStatus.ADAPTED
    assert adapted.budget == 12000
    assert len(adapted.adaptation_history) == 1

def test_stress_tester():
    tester = StressTester()
    scenario = StressScenario(
        scenario_id="stress-1",
        name="Market Crash",
        type=StressScenarioType.FINANCIAL,
        parameters={"revenue_drop_pct": 0.3}
    )
    tester.define_scenario(scenario)
    
    # Low cash reserves
    assessment = tester.run_stress_test("stress-1", current_cash_reserves=2000000, current_capacity=100)
    assert assessment.survivability_score == 0.4
    assert len(assessment.critical_failures) > 0

def test_action_ledger():
    ledger = ActionLedger(agent_budget=500.0)
    
    # L3 action within budget
    a1 = AutonomousAction(action_id="act-1", agent_id="agent-ops", action_type="restart_service", autonomy_level=AutonomyLevel.L3_AUTOMATE_LOW_RISK, budget_cost=10.0)
    res = ledger.propose_action(a1)
    assert res.status == ActionStatus.EXECUTED
    assert ledger.remaining_budget == 490.0
    
    # L5 action requiring human approval
    a2 = AutonomousAction(action_id="act-2", agent_id="agent-strat", action_type="reallocate_portfolio", autonomy_level=AutonomyLevel.L5_HIGH_IMPACT, budget_cost=0.0)
    res = ledger.propose_action(a2)
    assert res.status == ActionStatus.PROPOSED
    
    # Kill switch
    ledger.activate_kill_switch()
    a3 = AutonomousAction(action_id="act-3", agent_id="agent-ops", action_type="restart_service", autonomy_level=AutonomyLevel.L3_AUTOMATE_LOW_RISK, budget_cost=10.0)
    res = ledger.propose_action(a3)
    assert res.status == ActionStatus.BLOCKED
