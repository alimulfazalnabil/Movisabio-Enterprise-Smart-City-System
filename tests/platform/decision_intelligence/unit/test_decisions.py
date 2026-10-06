from datetime import datetime, timezone
from src.platform.decision_intelligence.engine.decision import DecisionEngine, Decision, DecisionOption, DecisionStatus
from src.platform.decision_intelligence.optimization.registry import OptimizationRegistry, OptimizationProblem
from src.platform.decision_intelligence.learning.outcome import DecisionLearner, DecisionOutcome
from src.platform.decision_intelligence.simulation.scenario import SimulationEngine

def test_decision_engine():
    engine = DecisionEngine()
    
    options = [
        DecisionOption(option_id="opt-a", description="Adaptive Signal", expected_impact={"delay": -18}, risk_level="Low", cost="Low"),
        DecisionOption(option_id="opt-b", description="Transit Priority", expected_impact={"delay": -4}, risk_level="Low", cost="Low")
    ]
    
    # We want to minimize delay (negative is better? wait, in our engine `score > best_score` means higher is better. 
    # Let's say objective is "throughput" for the test)
    options[0].expected_impact = {"throughput": 15}
    options[1].expected_impact = {"throughput": 5}
    
    decision = Decision(
        decision_id="dec-1",
        decision_type="TRAFFIC_OPT",
        tenant_id="t1",
        scope={},
        objective={"primary": "throughput"},
        constraints=[],
        options=options,
        created_at=datetime.now(timezone.utc)
    )
    
    evaluated = engine.evaluate_decision(decision)
    assert evaluated.status == DecisionStatus.EVALUATED
    assert evaluated.recommended_option_id == "opt-a"
    assert evaluated.options[0].is_recommended is True

def test_optimization_registry():
    registry = OptimizationRegistry()
    problem = OptimizationProblem(
        problem_id="traffic_coord",
        domain="traffic",
        objective={"minimize": ["delay"]},
        hard_constraints=["safety"],
        candidate_solvers=["PPO", "MILP"]
    )
    
    registry.register_problem(problem)
    solution = registry.solve("traffic_coord", {})
    assert solution["selected_solver"] == "PPO"
    assert "metrics" in solution

def test_decision_learner():
    learner = DecisionLearner()
    outcome = DecisionOutcome(
        outcome_id="out-1",
        decision_id="dec-1",
        expected_metrics={"delay_reduction": 20.0},
        actual_metrics={"delay_reduction": 15.0},
        outcome_status="COMPLETED",
        observed_at=datetime.now(timezone.utc)
    )
    
    deviations = learner.evaluate_outcome(outcome)
    # (15 - 20) / 20 = -0.25
    assert deviations["delay_reduction"] == -0.25

def test_simulation_engine():
    engine = SimulationEngine()
    options = [
        {"option_id": "opt-1", "base_score": 100},
        {"option_id": "opt-2", "base_score": 50}
    ]
    
    results = engine.simulate_options({}, options)
    assert len(results) == 2
    assert results[0].robustness_score > results[1].robustness_score
