"""Manage a small in-memory drone fleet and simulated dispatch missions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

@dataclass(frozen=True)
class DroneUnit:
    """Current state reported for one drone and its home station."""

    drone_id: str
    nest_station_id: str
    status: str  # STANDBY, DISPATCHED, EN_ROUTE, RETURNING, CHARGING
    battery_percentage: float
    current_gps_coordinates: tuple[float, float]
    altitude_meters: float

@dataclass(frozen=True)
class DroneMission:
    """Dispatch record and stream address for one reconnaissance mission."""

    mission_id: str
    drone_id: str
    target_intersection_id: str
    mission_type: str  # INCIDENT_RECONNAISSANCE, TRAFFIC_MONطرITORING, FLOOD_MAPPING
    rtsp_stream_url: str
    status: str
    dispatched_at: datetime = field(default_factory=datetime.utcnow)

class DroneOperationsEngine:
    """Select the first eligible standby drone from a process-local fleet."""

    def __init__(self):
        """Load the built-in demonstration fleet and an empty mission list."""

        # Simulated fleet inventory across municipal drone nests
        self.fleet: Dict[str, DroneUnit] = {
            "DRONE-01": DroneUnit("DRONE-01", "NEST-NORTH", "STANDBY", 98.5, (23.8103, 90.4125), 0.0),
            "DRONE-02": DroneUnit("DRONE-02", "NEST-CENTRAL", "STANDBY", 100.0, (23.8150, 90.4200), 0.0),
            "DRONE-03": DroneUnit("DRONE-03", "NEST-SOUTH", "CHARGING", 45.2, (23.8050, 90.4050), 0.0)
        }
        self.active_missions: List[DroneMission] = []

    def dispatch_reconnaissance_drone(self, target_intersection_id: str, mission_type: str = "INCIDENT_RECONNAISSANCE") -> Optional[DroneMission]:
        """Reserve an eligible drone and create a simulated mission.

        Returns:
            The new mission, or ``None`` when no standby drone has more than 30
            percent battery. This method does not contact a drone controller.
        """
        # Find available drone in standby
        available_drone_id = None
        for d_id, drone in self.fleet.items():
            if drone.status == "STANDBY" and drone.battery_percentage > 30.0:
                available_drone_id = d_id
                break

        if not available_drone_id:
            return None

        # Update drone state
        drone = self.fleet[available_drone_id]
        updated_drone = DroneUnit(
            drone_id=drone.drone_id,
            nest_station_id=drone.nest_station_id,
            status="DISPATCHED",
            battery_percentage=drone.battery_percentage,
            current_gps_coordinates=drone.current_gps_coordinates,
            altitude_meters=120.0
        )
        self.fleet[available_drone_id] = updated_drone

        mission = DroneMission(
            mission_id=f"MSN-{datetime.utcnow().strftime('%H%M%S')}-{available_drone_id}",
            drone_id=available_drone_id,
            target_intersection_id=target_intersection_id,
            mission_type=mission_type,
            rtsp_stream_url=f"rtsp://stream.movisabio.io/live/drone/{available_drone_id}/feed",
            status="ACTIVE"
        )
        self.active_missions.append(mission)
        return mission

    def get_fleet_telemetry(self) -> List[DroneUnit]:
        """Return a snapshot list of the process-local fleet values."""
        return list(self.fleet.values())
