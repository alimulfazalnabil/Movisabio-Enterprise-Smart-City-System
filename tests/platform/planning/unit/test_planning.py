from datetime import datetime, timezone
from src.platform.planning.engine.plan import PlanningEngine, Plan, PlanType, PlanStatus
from src.platform.planning.engine.replanning import ReplanningEngine
from src.platform.planning.interventions.intervention import Intervention, InterventionStatus
from src.platform.planning.metrics.kpi import TerritorialKPI, KPIManager
from src.platform.planning.governance.policy import PolicyGovernanceEngine, Policy, PolicyStatus

def test_planning_lifecycle():
    engine = PlanningEngine()
    plan = Plan(
        plan_id="p-1",
        tenant_id="t-1",
        twin_id="tw-1",
        name="Mobility 2030",
        plan_type=PlanType.STRATEGIC,
        objectives=[],
        created_at=datetime.now(timezone.utc)
    )
    engine.create_plan(plan)
    assert engine.plans["p-1"].status == PlanStatus.DRAFT
    
    engine.transition_state("p-1", PlanStatus.APPROVED)
    assert engine.plans["p-1"].status == PlanStatus.APPROVED

def test_replanning_trigger():
    planning_engine = PlanningEngine()
    planning_engine.create_plan(Plan(
        plan_id="p-1", tenant_id="t1", twin_id="tw1", name="Operational Plan",
        plan_type=PlanType.OPERATIONAL, objectives=[], created_at=datetime.now(timezone.utc)
    ))
    
    replan_engine = ReplanningEngine(planning_engine)
    triggered = replan_engine.evaluate_triggers("p-1", [{"type": "KPI_DEVIATION", "severity": "HIGH"}])
    
    assert triggered is True
    assert planning_engine.plans["p-1"].status == PlanStatus.ADAPTING

def test_kpi_evaluation():
    manager = KPIManager()
    kpi = TerritorialKPI(
        kpi_id="k-1", tenant_id="t1", domain="mobility", metric_name="delay", target_value=15.0, current_value=18.0
    )
    deviation = manager.evaluate_deviation(kpi)
    assert deviation == 0.2  # (18 - 15) / 15

def test_policy_governance():
    engine = PolicyGovernanceEngine()
    policy = Policy(policy_id="pol-1", name="Downtown Access", domain="traffic", rules=[])
    engine.submit_policy_proposal(policy)
    assert engine.policies["pol-1"].status == PolicyStatus.PROPOSED
    
    engine.approve_policy("pol-1", "user-gov")
    assert engine.policies["pol-1"].status == PolicyStatus.APPROVED
