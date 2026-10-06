from src.platform.execution.portfolio.portfolio_engine import PortfolioEngine, PortfolioItem, PortfolioHealth
from src.platform.execution.dependencies.dependency_engine import DependencyEngine, DependencyNode
from src.platform.execution.resources.allocation_engine import AllocationEngine, SkillRequirement
from src.platform.execution.benefits.benefit_engine import BenefitEngine, Benefit, BenefitStatus

def test_portfolio_engine():
    engine = PortfolioEngine()
    item = PortfolioItem(
        item_id="proj-1",
        name="Germany Expansion",
        item_type="PROJECT",
        strategic_objective_id="obj-1",
        budget_allocated=1000000,
        budget_spent=950000
    )
    engine.add_item(item)
    
    evaluated = engine.evaluate_health("proj-1")
    assert evaluated.health == PortfolioHealth.AT_RISK # Spent 95%
    
    evaluated.budget_spent = 1100000
    evaluated = engine.evaluate_health("proj-1")
    assert evaluated.health == PortfolioHealth.CRITICAL # Over budget

def test_dependency_engine():
    engine = DependencyEngine()
    
    engine.add_node(DependencyNode(node_id="infra", status="DELAYED"))
    engine.add_node(DependencyNode(node_id="api", depends_on=["infra"]))
    engine.add_node(DependencyNode(node_id="app", depends_on=["api"]))
    
    assert engine.check_blocked("api") is True
    assert engine.get_critical_path("app") == ["infra", "api", "app"]

def test_allocation_engine():
    engine = AllocationEngine()
    req = SkillRequirement(skill_name="ML_ENGINEER", required_count=5, available_count=2)
    engine.add_requirement(req)
    
    gaps = engine.analyze_gaps()
    assert gaps["ML_ENGINEER"] == 3
    assert engine.recommend_action("ML_ENGINEER") == "INTERNAL_TRAINING_OR_CONTRACTOR"

def test_benefit_engine():
    engine = BenefitEngine()
    benefit = Benefit(
        benefit_id="ben-1",
        project_id="proj-1",
        expected_value=1000,
        observed_value=200,
        project_status="COMPLETED"
    )
    engine.add_benefit(benefit)
    
    evaluated = engine.detect_leakage("ben-1")
    assert evaluated.status == BenefitStatus.LEAKING # 20% is < 30% threshold for completed project
