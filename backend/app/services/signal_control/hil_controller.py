from typing import Dict, Any
from .controller import SignalController
from backend.app.simulation.adapters import SimulationAdapter

class HILController(SignalController):
    """
    Hardware-in-the-Loop Gateway.
    Passes commands to an actual signal controller via a protocol adapter (e.g. NTCIP),
    while synchronizing state back to the simulation (SUMO).
    """
    def __init__(self, physical_adapter, simulation_adapter: SimulationAdapter):
        self.physical = physical_adapter
        self.sumo = simulation_adapter
        self.executed_commands = set()

    def get_state(self, intersection_id: str) -> Dict[str, Any]:
        return self.physical.read_state(intersection_id)

    def send_command(self, intersection_id: str, command: Dict[str, Any]) -> bool:
        cmd_id = command.get("command_id")
        if cmd_id and cmd_id in self.executed_commands:
            return False
            
        phase = command.get("requested_phase")
        duration = command.get("duration", 30.0)
        
        # 1. Send to Physical Testbed
        success = self.physical.send_phase_command(intersection_id, phase, duration)
        
        # 2. Sync to SUMO Simulation
        if success:
            self.sumo.set_signal_state(intersection_id, phase, duration)
            if cmd_id:
                self.executed_commands.add(cmd_id)
                
        return success

    def verify_command(self, intersection_id: str, command_id: str) -> bool:
        return self.physical.verify(intersection_id, command_id)

    def health_check(self, intersection_id: str) -> bool:
        return self.physical.health(intersection_id)

    def emergency_stop(self, intersection_id: str) -> bool:
        return self.physical.emergency_stop(intersection_id)
