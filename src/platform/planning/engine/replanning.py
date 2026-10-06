from typing import Dict, Any, List
from datetime import datetime
from src.platform.planning.engine.plan import Plan, PlanStatus

class ReplanningTrigger(Dict[str, Any]):
    pass

class ReplanningEngine:
    def __init__(self, planning_engine):
        self.planning_engine = planning_engine
        
    def evaluate_triggers(self, plan_id: str, triggers: List[ReplanningTrigger]) -> bool:
        """
        Evaluates triggers (KPI deviations, events) to decide if replanning is needed.
        """
        plan = self.planning_engine.plans.get(plan_id)
        if not plan:
            return False
            
        requires_replan = False
        for trigger in triggers:
            if trigger.get("type") == "KPI_DEVIATION" and trigger.get("severity") == "HIGH":
                requires_replan = True
                break
                
        if requires_replan:
            self.planning_engine.transition_state(plan_id, PlanStatus.ADAPTING)
            
        return requires_replan
