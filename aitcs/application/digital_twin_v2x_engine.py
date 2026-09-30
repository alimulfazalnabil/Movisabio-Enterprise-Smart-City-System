"""In-memory V2X buffer and deterministic digital-twin step simulator."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

@dataclass(frozen=True)
class V2XBasicSafetyMessage:
    """Subset of vehicle position and motion data used by the simulator."""

    vehicle_id: str
    latitude: float
    longitude: float
    speed_ms: float
    heading_degrees: float
    acceleration_mps2: float
    intersection_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(frozen=True)
class SimulationSyncState:
    """Summary returned after advancing the local simulation counter."""

    simulation_engine: str  # SUMO or CARLA
    simulation_step: int
    active_vehicles_simulated: int
    mean_travel_time_seconds: float
    synchronization_status: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class DigitalTwinV2XEngine:
    """Buffer recent V2X messages and expose a simulated synchronization step."""

    def __init__(self):
        """Create an empty 1,000-message buffer and reset the step counter."""

        self.current_step = 0
        self.v2x_messages_buffer: List[V2XBasicSafetyMessage] = []

    def ingest_v2x_bsm(self, bsm: V2XBasicSafetyMessage) -> bool:
        """Append a safety message, discard the oldest on overflow and return true."""
        self.v2x_messages_buffer.append(bsm)
        if len(self.v2x_messages_buffer) > 1000:
            self.v2x_messages_buffer.pop(0)
        return True

    def sync_simulation_step(self, engine_type: str = "SUMO") -> SimulationSyncState:
        """Advance the local counter and return deterministic simulated metrics.

        No SUMO or CARLA process is contacted by this implementation.
        """
        self.current_step += 1
        sim_name = engine_type.upper()
        
        return SimulationSyncState(
            simulation_engine=sim_name,
            simulation_step=self.current_step,
            active_vehicles_simulated=1420 + (self.current_step % 50),
            mean_travel_time_seconds=184.5 - (self.current_step % 10) * 0.2,
            synchronization_status="SYNCHRONIZED_ACTIVE"
        )
