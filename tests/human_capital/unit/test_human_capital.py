from src.services.human_capital.models.schemas import SkillDemand, SkillSupply, WorkforceScenario
from src.services.human_capital.engine.skills_gap import SkillsGapEngine
from src.services.human_capital.engine.scenario import WorkforceScenarioEngine

def test_skills_gap_calculation():
    demand = SkillDemand(skill_id="SKILL-PYTHON", territory_id="TERR-1", estimated_demand=1000.0, period="2027")
    supply = SkillSupply(skill_id="SKILL-PYTHON", territory_id="TERR-1", effective_supply=700.0, period="2027")
    
    engine = SkillsGapEngine()
    gap = engine.calculate_gap(demand, supply)
    
    assert gap.gap_value == 300.0
    # 300 is 30% of 1000, which is > 20%, so HIGH_SHORTAGE
    assert gap.status == "HIGH_SHORTAGE"
    
    # Test surplus
    supply_surplus = SkillSupply(skill_id="SKILL-PYTHON", territory_id="TERR-1", effective_supply=1500.0, period="2027")
    gap_surplus = engine.calculate_gap(demand, supply_surplus)
    assert gap_surplus.status == "SURPLUS"

def test_workforce_scenario_training_requirements():
    scenario = WorkforceScenario(
        scenario_id="SCENARIO-EV-FACTORY",
        industry="MANUFACTURING",
        new_jobs=2000,
        required_skills={
            "SKILL-ROBOTICS": 0.50, # 50% need robotics
            "SKILL-ELECTRICAL": 0.80 # 80% need electrical
        }
    )
    
    engine = WorkforceScenarioEngine()
    reqs = engine.simulate_training_requirements(scenario)
    
    assert reqs["SKILL-ROBOTICS"] == 1000.0
    assert reqs["SKILL-ELECTRICAL"] == 1600.0
