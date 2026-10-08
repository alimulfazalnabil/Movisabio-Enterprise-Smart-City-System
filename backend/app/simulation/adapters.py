"""TraCI-backed simulation boundary for MoviSabio.

SUMO remains behind this adapter so application/domain code does not depend on
TraCI. No SUMO process is started at import time.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os


@dataclass(frozen=True)
class SimulationStepResult:
    simulation_time_s: float
    remaining_vehicles: int
    vehicle_count: int


@dataclass(frozen=True)
class SimulationSignalState:
    intersection_id: str
    phase_index: int | None
    phase_name: str | None
    phase_duration_s: float | None
    simulation_time_s: float | None


class SimulationAdapter(ABC):
    """Stable boundary for replay, mock, and SUMO simulation backends."""

    @abstractmethod
    def start_simulation(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def step(self, step_length_s: float = 1.0) -> SimulationStepResult:
        raise NotImplementedError

    @abstractmethod
    def get_vehicle_state(self) -> dict[str, dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_signal_state(self, intersection_id: str) -> SimulationSignalState:
        raise NotImplementedError

    @abstractmethod
    def set_signal_state(self, intersection_id: str, phase: int, duration: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class SUMOAdapter(SimulationAdapter):
    """Concrete SUMO/TraCI implementation.

    The adapter validates its configuration before starting SUMO and exposes
    only simulation operations to callers. It never connects to a physical
    traffic controller.
    """

    def __init__(
        self,
        config_path: str,
        *,
        binary: str | None = None,
        seed: int | None = None,
        label: str = "movisabio",
        extra_args: list[str] | None = None,
    ) -> None:
        self.config_path = Path(config_path)
        self.binary = binary or os.getenv("SUMO_BINARY", "sumo")
        self.seed = seed
        self.label = label
        self.extra_args = extra_args or []
        self._traci = None
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            raise RuntimeError("SUMO is not running; call start_simulation() first.")
        return self._connection

    def _load_traci(self):
        try:
            import traci
        except ImportError as exc:
            raise RuntimeError(
                "TraCI is not installed. Install the 'traci' package to use SUMO."
            ) from exc
        self._traci = traci
        return traci

    def start_simulation(self) -> None:
        if not self.config_path.is_file():
            raise FileNotFoundError(
                f"SUMO configuration file does not exist: {self.config_path}"
            )

        traci = self._load_traci()
        if self._connection is not None:
            return

        args = [
            self.binary,
            "-c",
            str(self.config_path),
            "--quit-on-end",
            "true",
        ]
        if self.seed is not None:
            args.extend(["--seed", str(self.seed)])
        args.extend(self.extra_args)

        try:
            traci.start(args, label=self.label)
            self._connection = traci.getConnection(self.label)
        except Exception:
            self._connection = None
            raise

    def step(self, step_length_s: float = 1.0) -> SimulationStepResult:
        if step_length_s <= 0:
            raise ValueError("step_length_s must be greater than zero")

        conn = self.connection
        target_time = conn.simulation.getTime() + step_length_s
        conn.simulationStep(target_time)

        return SimulationStepResult(
            simulation_time_s=float(conn.simulation.getTime()),
            remaining_vehicles=int(conn.simulation.getMinExpectedNumber()),
            vehicle_count=len(conn.vehicle.getIDList()),
        )

    def get_vehicle_state(self) -> dict[str, dict[str, Any]]:
        conn = self.connection
        result: dict[str, dict[str, Any]] = {}

        for vehicle_id in conn.vehicle.getIDList():
            x, y = conn.vehicle.getPosition(vehicle_id)
            result[vehicle_id] = {
                "vehicle_id": vehicle_id,
                "edge_id": conn.vehicle.getRoadID(vehicle_id),
                "lane_id": conn.vehicle.getLaneID(vehicle_id),
                "position_x_m": float(x),
                "position_y_m": float(y),
                "speed_mps": float(conn.vehicle.getSpeed(vehicle_id)),
            }

        return result

    def get_signal_state(self, intersection_id: str) -> SimulationSignalState:
        conn = self.connection
        phase_index = int(conn.trafficlight.getPhase(intersection_id))
        phase_duration = float(conn.trafficlight.getPhaseDuration(intersection_id))
        simulation_time = float(conn.simulation.getTime())

        try:
            phase_name = conn.trafficlight.getPhaseName(intersection_id)
        except (AttributeError, self._traci.TraCIException):
            phase_name = None

        return SimulationSignalState(
            intersection_id=intersection_id,
            phase_index=phase_index,
            phase_name=phase_name,
            phase_duration_s=phase_duration,
            simulation_time_s=simulation_time,
        )

    def set_signal_state(self, intersection_id: str, phase: int, duration: float) -> None:
        if phase < 0:
            raise ValueError("phase must be non-negative")
        if duration <= 0:
            raise ValueError("duration must be greater than zero")

        conn = self.connection
        conn.trafficlight.setPhase(intersection_id, int(phase))
        conn.trafficlight.setPhaseDuration(intersection_id, float(duration))

    def close(self) -> None:
        if self._connection is None:
            return
        try:
            self._connection.close()
        finally:
            self._connection = None
            self._traci = None

    def __enter__(self) -> "SUMOAdapter":
        self.start_simulation()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
