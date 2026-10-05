from src.services.culture.models.schemas import CulturalEvent, EventImpactSimulation

class EventImpactEngine:
    def simulate_impact(self, event: CulturalEvent) -> EventImpactSimulation:
        """
        Simulates the estimated demands placed on the territory by an event.
        """
        # Simplistic multipliers for simulation purposes
        transit_demand = event.expected_capacity * 0.6 # 60% use transit
        waste_demand = event.expected_capacity * 0.5 # kg per person
        energy_demand = event.expected_capacity * 2.0 # kWh per person
        
        return EventImpactSimulation(
            event_id=event.event_id,
            transit_demand=transit_demand,
            waste_demand=waste_demand,
            energy_demand=energy_demand
        )
