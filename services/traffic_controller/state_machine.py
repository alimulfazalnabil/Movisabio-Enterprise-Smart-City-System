import enum
import time
from pydantic import BaseModel
from typing import Dict, Any

class SignalState(str, enum.Enum):
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    ALL_RED = "ALL_RED"

class MockTrafficController:
    """
    Phase 5 / Sprint 2: Traffic Controller Simulator.
    Simulates physical traffic lights and handles ACK/NACK, timeouts, etc.
    """
    def __init__(self):
        self.current_phase = "EW_GREEN"
        self.state = SignalState.GREEN
        
    def set_phase(self, requested_phase: str, command_id: str) -> Dict[str, Any]:
        """
        Simulates receiving a command and transitioning phases.
        Transitions: GREEN -> YELLOW -> ALL_RED -> GREEN (new phase)
        """
        # Mock immediate ACK response
        print(f"[Controller] Received CMD: {command_id} to switch to {requested_phase}")
        
        if self.current_phase == requested_phase:
            return {
                "command_id": command_id,
                "status": "NACK",
                "reason": "Phase already active"
            }
            
        print(f"[Controller] Transitioning: {self.current_phase} (GREEN -> YELLOW)")
        self.state = SignalState.YELLOW
        # In real life, sleep for Yellow duration
        
        print(f"[Controller] Transitioning: {self.current_phase} (YELLOW -> ALL_RED)")
        self.state = SignalState.ALL_RED
        # In real life, sleep for All-Red clearance duration
        
        self.current_phase = requested_phase
        self.state = SignalState.GREEN
        print(f"[Controller] Transition Complete: {self.current_phase} is now GREEN")
        
        return {
            "command_id": command_id,
            "status": "ACCEPTED",
            "phase": requested_phase
        }
