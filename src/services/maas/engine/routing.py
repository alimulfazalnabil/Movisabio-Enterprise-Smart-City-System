import uuid
from typing import List, Dict
from src.services.maas.models.schemas import JourneyPlan, JourneyLeg

class MultimodalRoutingEngine:
    """
    Constructs multimodal journey alternatives based on user objectives.
    """
    
    def generate_alternatives(self, origin: str, destination: str, objective: str = "FASTEST") -> List[JourneyPlan]:
        """
        Mock generator for multimodal routes.
        In reality, this traverses the MobilityGraph combining road, transit, and shared mobility nodes.
        """
        # Mock Alternative A: Transit
        leg_a1 = JourneyLeg(
            mode="WALK", origin=origin, destination="STOP_1", start_time="2026-10-02T08:00:00Z", end_time="2026-10-02T08:05:00Z", 
            travel_time_sec=300, cost=0.0, provider_id="USER", emissions_estimate=0.0, distance_meters=400
        )
        leg_a2 = JourneyLeg(
            mode="BUS", origin="STOP_1", destination="STOP_2", start_time="2026-10-02T08:05:00Z", end_time="2026-10-02T08:25:00Z", 
            travel_time_sec=1200, cost=2.40, provider_id="TRANSIT_AGENCY", emissions_estimate=0.5, distance_meters=5000
        )
        
        plan_a = JourneyPlan(
            plan_id=str(uuid.uuid4()),
            origin=origin, destination=destination,
            legs=[leg_a1, leg_a2],
            total_travel_time_sec=1500,
            total_cost=2.40,
            total_emissions=0.5,
            transfers=1,
            score=0.9 if objective == "CHEAPEST" else 0.7
        )
        
        # Mock Alternative B: Ride-hailing
        leg_b1 = JourneyLeg(
            mode="TAXI", origin=origin, destination=destination, start_time="2026-10-02T08:00:00Z", end_time="2026-10-02T08:20:00Z", 
            travel_time_sec=1200, cost=15.00, provider_id="RIDESHARE_INC", emissions_estimate=2.5, distance_meters=6000
        )
        
        plan_b = JourneyPlan(
            plan_id=str(uuid.uuid4()),
            origin=origin, destination=destination,
            legs=[leg_b1],
            total_travel_time_sec=1200,
            total_cost=15.00,
            total_emissions=2.5,
            transfers=0,
            score=0.9 if objective == "FASTEST" else 0.4
        )
        
        # Sort by score descending
        return sorted([plan_a, plan_b], key=lambda x: x.score, reverse=True)
