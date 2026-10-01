from src.services.energy.models.schemas import EnergyState

class GridConstraintEngine:
    """
    Evaluates site-level energy balance and prevents grid overloads.
    """
    
    def evaluate_capacity(self, state: EnergyState, max_grid_connection_kw: float) -> float:
        """
        Site-level Energy Balance:
        Generation + Grid Import + Battery Discharge = EV Load + Building Load + Battery Charge + Grid Export
        
        Returns available capacity for EV charging.
        """
        current_load = state.building_load_kw + state.battery_charge_kw + state.grid_export_kw
        current_generation = state.renewable_generation_kw + state.battery_discharge_kw
        
        net_load_on_grid = current_load - current_generation
        
        available_capacity = max_grid_connection_kw - net_load_on_grid
        
        return max(0.0, available_capacity)
