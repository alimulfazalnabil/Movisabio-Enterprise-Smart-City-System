from src.services.human_capital.models.schemas import WorkforceScenario
from typing import Dict

class WorkforceScenarioEngine:
    def simulate_training_requirements(self, scenario: WorkforceScenario) -> Dict[str, float]:
        """
        Calculates the number of required workers per skill for a given scenario.
        """
        requirements = {}
        for skill_id, percentage in scenario.required_skills.items():
            requirements[skill_id] = scenario.new_jobs * percentage
            
        return requirements
