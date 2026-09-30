"""Estimate local emissions and weather effects from traffic measurements."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

@dataclass(frozen=True)
class EnvironmentalMetrics:
    """Heuristic environmental estimates for one intersection."""

    intersection_id: str
    co2_estimation_kg_h: float
    pm25_ug_m3: float
    no_estimation_g_h: float
    fuel_consumption_liters_h: float
    weather_condition: str
    timing_multiplier: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

class EnvironmentalWeatherEngine:
    """Apply deterministic traffic and weather multipliers to emissions."""

    def __init__(self):
        """Initialize the supported weather-condition multipliers."""

        self.weather_multipliers = {
            "CLEAR": 1.0,
            "RAIN": 1.25,
            "FOG": 1.35,
            "SNOW": 1.50
        }

    def compute_environmental_impact(
        self, intersection_id: str, vehicle_count: int, avg_speed_kmh: float, weather_condition: str = "CLEAR"
    ) -> EnvironmentalMetrics:
        """Estimate emissions, fuel use and a timing multiplier.

        Args:
            intersection_id: Location represented by the metrics.
            vehicle_count: Vehicles observed in the sampling interval.
            avg_speed_kmh: Mean vehicle speed in kilometres per hour.
            weather_condition: Condition name; unknown values behave as clear.

        Returns:
            Heuristic metrics intended for simulation and relative comparison,
            not calibrated environmental measurements.
        """
        condition = weather_condition.upper()
        multiplier = self.weather_multipliers.get(condition, 1.0)

        # Idling penalty increases when average speed drops below 20 km/h
        idling_factor = max(1.0, (40.0 - min(40.0, avg_speed_kmh)) / 10.0)
        
        co2 = round(vehicle_count * 0.15 * idling_factor * multiplier, 2)
        pm25 = round(15.0 + (vehicle_count * 0.4 * idling_factor), 2)
        no_gas = round(vehicle_count * 0.05 * idling_factor, 2)
        fuel = round(vehicle_count * 0.08 * idling_factor, 2)

        return EnvironmentalMetrics(
            intersection_id=intersection_id,
            co2_estimation_kg_h=co2,
            pm25_ug_m3=pm25,
            no_estimation_g_h=no_gas,
            fuel_consumption_liters_h=fuel,
            weather_condition=condition,
            timing_multiplier=multiplier
        )
