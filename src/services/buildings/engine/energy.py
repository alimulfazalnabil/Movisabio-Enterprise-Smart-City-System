from src.services.buildings.models.schemas import BuildingEnergy

class EnergyManagementEngine:
    """
    Manages building energy and coordinates Demand Response.
    """
    
    def evaluate_demand_response(self, energy: BuildingEnergy, grid_critical: bool) -> BuildingEnergy:
        """
        Activates or deactivates Demand Response based on grid conditions.
        """
        if grid_critical and not energy.dr_active:
            energy.dr_active = True
            # Simulate a 20% reduction target
            energy.current_kw = energy.baseline_kw * 0.8
        elif not grid_critical and energy.dr_active:
            energy.dr_active = False
            energy.current_kw = energy.baseline_kw
            
        return energy
