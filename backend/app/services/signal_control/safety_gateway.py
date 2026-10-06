from typing import Dict, Any
from .controller import SignalController

class SafetyGateway(SignalController):
    """
    Decorator for SignalController that enforces hard physical safety boundaries 
    before dispatching to the underlying controller.
    """
    def __init__(self, underlying_controller: SignalController, config: Dict[str, Any]):
        self.underlying = underlying_controller
        self.config = config
        
        # Hard limits
        self.min_green = self.config.get("min_green", 5.0)
        self.max_green = self.config.get("max_green", 180.0)

    def get_state(self, intersection_id: str) -> Dict[str, Any]:
        return self.underlying.get_state(intersection_id)

    def send_command(self, intersection_id: str, command: Dict[str, Any]) -> bool:
        # B6.5 Hard Safety Boundaries
        
        # 1. Check Duration Limits
        duration = command.get("duration", 0)
        if duration < self.min_green:
            print(f"Safety Reject: Requested green {duration}s < {self.min_green}s")
            return False
            
        if duration > self.max_green:
            print(f"Safety Reject: Requested green {duration}s > {self.max_green}s")
            return False
            
        # 2. Controller Health
        if not self.health_check(intersection_id):
            print("Safety Reject: Controller is offline or unhealthy.")
            return False
            
        # 3. Valid Optimization
        if command.get("safety_result") != "VALIDATED":
            print("Safety Reject: Command lacked upstream safety validation signature.")
            return False

        # Passes boundaries, dispatch to underlying
        return self.underlying.send_command(intersection_id, command)

    def verify_command(self, intersection_id: str, command_id: str) -> bool:
        return self.underlying.verify_command(intersection_id, command_id)

    def health_check(self, intersection_id: str) -> bool:
        return self.underlying.health_check(intersection_id)

    def emergency_stop(self, intersection_id: str) -> bool:
        # Unconditionally allowed through
        return self.underlying.emergency_stop(intersection_id)
