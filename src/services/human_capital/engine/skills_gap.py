from src.services.human_capital.models.schemas import SkillDemand, SkillSupply, SkillGap
import uuid

class SkillsGapEngine:
    def calculate_gap(self, demand: SkillDemand, supply: SkillSupply) -> SkillGap:
        """
        Calculates the gap between skill demand and effective supply.
        """
        if demand.skill_id != supply.skill_id or demand.territory_id != supply.territory_id:
            raise ValueError("Mismatched demand and supply records")

        gap_value = demand.estimated_demand - supply.effective_supply
        
        status = "BALANCED"
        if gap_value > (0.2 * demand.estimated_demand):
            status = "HIGH_SHORTAGE"
        elif gap_value > 0:
            status = "MODERATE_SHORTAGE"
        elif gap_value < -(0.2 * supply.effective_supply):
            status = "SURPLUS"
            
        return SkillGap(
            gap_id=str(uuid.uuid4()),
            skill_id=demand.skill_id,
            territory_id=demand.territory_id,
            estimated_demand=demand.estimated_demand,
            effective_supply=supply.effective_supply,
            gap_value=gap_value,
            status=status
        )
