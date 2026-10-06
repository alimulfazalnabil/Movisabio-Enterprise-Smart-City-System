from src.platform.customer_success.health.score import HealthEngine, HealthState
from src.platform.customer_success.onboarding.project import OnboardingManager, OnboardingProject, OnboardingMilestone, MilestoneStatus
from src.platform.customer_success.outcomes.intelligence import OutcomeEngine, CustomerOutcome, AttributionLevel
from src.platform.customer_success.renewal.intelligence import RenewalEngine, RenewalOpportunity, RenewalRisk
from datetime import datetime, timezone, timedelta

def test_health_engine():
    engine = HealthEngine()
    record = engine.calculate_health("cust-1", {"adoption": 90, "support": 100})
    assert record.overall_score == 95
    assert record.state == HealthState.HEALTHY
    
    record = engine.calculate_health("cust-2", {"adoption": 20, "support": 40})
    assert record.overall_score == 30
    assert record.state == HealthState.CRITICAL

def test_onboarding_manager():
    manager = OnboardingManager()
    project = OnboardingProject(
        project_id="proj-1",
        customer_id="cust-1",
        tenant_id="t-1",
        milestones={
            "m-1": OnboardingMilestone(milestone_id="m-1", name="Kickoff"),
            "m-2": OnboardingMilestone(milestone_id="m-2", name="Go Live")
        }
    )
    manager.create_project(project)
    manager.complete_milestone("proj-1", "m-1")
    assert not manager.projects["proj-1"].is_live
    manager.complete_milestone("proj-1", "m-2")
    assert manager.projects["proj-1"].is_live

def test_outcome_engine():
    engine = OutcomeEngine()
    outcome = CustomerOutcome(
        outcome_id="out-1",
        customer_id="cust-1",
        objective="Reduce delay",
        metric="delay_min",
        baseline=18.2,
        target=15.0
    )
    engine.register_outcome(outcome)
    engine.record_measurement("out-1", 15.8, AttributionLevel.PARTIALLY_ATTRIBUTED, "Sensor data")
    assert engine.outcomes["out-1"].observed == 15.8
    assert engine.outcomes["out-1"].attribution == AttributionLevel.PARTIALLY_ATTRIBUTED

def test_renewal_intelligence():
    engine = RenewalEngine()
    opp = RenewalOpportunity(
        renewal_id="ren-1",
        customer_id="cust-1",
        subscription_id="sub-1",
        expiry_date=datetime.now(timezone.utc) + timedelta(days=30)
    )
    res = engine.analyze_renewal(opp, health_score=50, open_p1_tickets=1)
    assert res.risk == RenewalRisk.CRITICAL
