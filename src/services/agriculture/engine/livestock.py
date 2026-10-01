from src.services.agriculture.models.schemas import Livestock, FenceState

class VirtualFenceEngine:
    """
    State machine for livestock virtual fencing.
    """
    
    def evaluate_position(self, animal: Livestock, distance_to_boundary_m: float, moving_towards_boundary: bool) -> Livestock:
        current_state = animal.fence_state
        
        if current_state == FenceState.NORMAL:
            if distance_to_boundary_m < 50.0 and moving_towards_boundary:
                animal.fence_state = FenceState.APPROACHING_BOUNDARY
                
        elif current_state == FenceState.APPROACHING_BOUNDARY:
            if distance_to_boundary_m < 20.0 and moving_towards_boundary:
                animal.fence_state = FenceState.BOUNDARY_WARNING
            elif not moving_towards_boundary and distance_to_boundary_m > 30.0:
                animal.fence_state = FenceState.NORMAL
                
        elif current_state == FenceState.BOUNDARY_WARNING:
            if distance_to_boundary_m <= 0.0:
                animal.fence_state = FenceState.BOUNDARY_BREACH_CANDIDATE
            elif not moving_towards_boundary and distance_to_boundary_m > 30.0:
                animal.fence_state = FenceState.NORMAL
                
        elif current_state == FenceState.BOUNDARY_BREACH_CANDIDATE:
            # Requires explicit confirmation to move to INTERVENTION
            pass
            
        elif current_state == FenceState.INTERVENTION:
            if not moving_towards_boundary and distance_to_boundary_m > 20.0:
                animal.fence_state = FenceState.RETURNING
                
        elif current_state == FenceState.RETURNING:
            if distance_to_boundary_m > 50.0:
                animal.fence_state = FenceState.NORMAL
                
        return animal
