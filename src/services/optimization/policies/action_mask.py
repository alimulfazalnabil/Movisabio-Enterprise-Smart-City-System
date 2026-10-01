from typing import List, Dict
from .action_space import OptimizerAction

class ActionMask:
    """
    Evaluates which OptimizerActions are valid in the current controller state.
    """
    
    def __init__(self, min_green_sec: float = 10.0, max_green_sec: float = 60.0):
        self.min_green_sec = min_green_sec
        self.max_green_sec = max_green_sec

    def generate_mask(self, phase_elapsed: float) -> List[bool]:
        """
        Returns a boolean mask aligned with the OptimizerAction IntEnum.
        True = Allowed, False = Blocked.
        """
        mask = [False] * len(OptimizerAction)
        
        # Can always hold, unless we hit max green
        if phase_elapsed < self.max_green_sec:
            mask[OptimizerAction.HOLD] = True
            
        # Can extend if we don't exceed max green
        if phase_elapsed + 5.0 <= self.max_green_sec:
            mask[OptimizerAction.EXTEND_5] = True
            
        if phase_elapsed + 10.0 <= self.max_green_sec:
            mask[OptimizerAction.EXTEND_10] = True
            
        # Can only terminate or change if minimum green has elapsed
        if phase_elapsed >= self.min_green_sec:
            mask[OptimizerAction.TERMINATE] = True
            mask[OptimizerAction.SELECT_NEXT] = True
            
        return mask
