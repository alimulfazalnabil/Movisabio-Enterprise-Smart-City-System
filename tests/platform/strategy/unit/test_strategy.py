from src.platform.strategy.decisions.decision_engine import DecisionEngine, StrategicDecision, DecisionStatus
from src.platform.strategy.scenarios.scenario_engine import ScenarioEngine, Scenario, ScenarioType
from src.platform.strategy.investment.portfolio import PortfolioOptimizer, InvestmentOpportunity, InvestmentStatus
from src.platform.strategy.drift.detector import StrategyDriftEngine, StrategyMetric, StrategyDriftStatus

def test_decision_engine():
    engine = DecisionEngine()
    dec = StrategicDecision(
        decision_id="dec-1",
        owner="exec-team",
        question="Which region to expand next?",
        options=["Region A", "Region B", "Defer"]
    )
    engine.create_decision(dec)
    
    updated = engine.recommend("dec-1", "Region A", "HIGH")
    assert updated.status == DecisionStatus.PROPOSED
    assert updated.recommendation == "Region A"

def test_scenario_engine():
    engine = ScenarioEngine()
    scenario = Scenario(
        scenario_id="scen-1",
        name="High Growth",
        scenario_type=ScenarioType.GROWTH,
        assumptions={"customer_growth_rate": 2.0, "cloud_cost_increase": 1.5}
    )
    engine.create_scenario(scenario)
    
    simulated = engine.simulate("scen-1", base_revenue=100000, base_cost=60000)
    assert simulated.projected_revenue == 200000
    assert simulated.projected_cost == 90000
    assert simulated.projected_risk_score == 0.2

def test_portfolio_optimizer():
    optimizer = PortfolioOptimizer()
    opp1 = InvestmentOpportunity(
        investment_id="inv-1",
        name="AI Expansion",
        capital_required=500000,
        expected_value=2000000,
        risk_score=0.5,
        strategic_alignment=0.9
    )
    opp2 = InvestmentOpportunity(
        investment_id="inv-2",
        name="Legacy Migration",
        capital_required=300000,
        expected_value=400000,
        risk_score=0.1,
        strategic_alignment=0.8
    )
    optimizer.add_opportunity(opp1)
    optimizer.add_opportunity(opp2)
    
    # Budget constraint of 600k, should pick the one with better risk-adjusted value
    selected = optimizer.optimize_portfolio(600000)
    assert len(selected) == 1
    assert selected[0].investment_id == "inv-1"
    
    # opp2 should be deferred
    assert optimizer.opportunities["inv-2"].status == InvestmentStatus.DEFERRED

def test_drift_detector():
    engine = StrategyDriftEngine()
    # Expected 20% growth, actual 8%
    metric = engine.record_observation("met-1", "Customer Growth", 0.20, 0.08)
    
    # variance = |0.08 - 0.20| / 0.20 = 0.6. Threshold is 0.1
    assert metric.variance == 0.6
    assert metric.status == StrategyDriftStatus.DRIFT_DETECTED
    assert engine.check_overall_drift() is True
