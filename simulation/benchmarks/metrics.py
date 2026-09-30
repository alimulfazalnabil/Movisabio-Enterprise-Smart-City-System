from pydantic import BaseModel
from typing import Dict

class BenchmarkMetrics(BaseModel):
    average_delay_seconds: float
    percentile_95_delay_seconds: float
    max_queue_length: int
    average_travel_time_seconds: float
    throughput_vehicles_per_hour: float
    average_stops_per_vehicle: float
    fuel_consumption_liters: float
    co2_emissions_kg: float
    fairness_index: float
    emergency_response_time_seconds: float

class BenchmarkEngine:
    """
    Evaluates Candidate vs Baselines in SUMO (Fixed-time, Actuated, MoviSabio).
    """
    def __init__(self):
        self.metrics_store = []

    def compute_metrics(self, sumo_traci_output: Dict) -> BenchmarkMetrics:
        """
        Parses raw SUMO output and calculates the KPIs required for the safety case.
        """
        # Mock calculation from TraCI outputs
        return BenchmarkMetrics(
            average_delay_seconds=sumo_traci_output.get("delay", 15.0),
            percentile_95_delay_seconds=sumo_traci_output.get("delay_95", 45.0),
            max_queue_length=sumo_traci_output.get("queue", 10),
            average_travel_time_seconds=sumo_traci_output.get("travel_time", 120.0),
            throughput_vehicles_per_hour=sumo_traci_output.get("throughput", 1200.0),
            average_stops_per_vehicle=sumo_traci_output.get("stops", 1.2),
            fuel_consumption_liters=sumo_traci_output.get("fuel", 50.0),
            co2_emissions_kg=sumo_traci_output.get("co2", 115.0),
            fairness_index=sumo_traci_output.get("fairness", 0.85),
            emergency_response_time_seconds=sumo_traci_output.get("emergency", 30.0)
        )
