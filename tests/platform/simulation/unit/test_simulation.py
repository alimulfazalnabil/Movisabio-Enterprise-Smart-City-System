from datetime import datetime
from src.platform.digital_twin.state.snapshot import TwinStateEngine, StateType
from src.platform.simulation.orchestrator.scenario import ScenarioEngine, Scenario
from src.platform.simulation.engines.base import SUMOEngineAdapter
from src.platform.simulation.calibration.validator import ModelValidator

def test_twin_snapshot():
    engine = TwinStateEngine()
    snapshot = engine.create_snapshot("twin-mvd", StateType.CURRENT, {"traffic_level": "high"})
    assert snapshot.state_type == StateType.CURRENT
    assert snapshot.twin_id == "twin-mvd"

def test_scenario_branching():
    engine = ScenarioEngine()
    base_scenario = Scenario(
        scenario_id="scen-base",
        name="Baseline",
        tenant_id="t1",
        twin_id="twin-1",
        baseline_snapshot_id="snap-1",
        interventions=[{"type": "road_closure"}],
        simulation_engines=["sumo"]
    )
    engine.create_scenario(base_scenario)
    
    branched = engine.branch_scenario("scen-base", "With Signal Opt", [{"type": "signal_optimization"}])
    assert branched.parent_scenario_id == "scen-base"
    assert len(branched.interventions) == 2
    assert branched.interventions[1]["type"] == "signal_optimization"

def test_sumo_adapter():
    adapter = SUMOEngineAdapter()
    adapter.prepare({})
    adapter.initialize({})
    adapter.step(1)
    results = adapter.get_results()
    assert results["avg_speed"] == 35.5

def test_model_validator():
    validator = ModelValidator()
    observed = {"speed": 30.0, "delay": 100.0}
    simulated = {"speed": 27.0, "delay": 110.0}
    
    errors = validator.validate_simulation(observed, simulated)
    # speed error: |30 - 27| / 30 = 0.1
    # delay error: |100 - 110| / 100 = 0.1
    assert errors["speed"] == 0.1
    assert errors["delay"] == 0.1
