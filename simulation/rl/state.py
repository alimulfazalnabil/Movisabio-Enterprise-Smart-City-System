import numpy as np
from typing import Dict

class RLStateBuilder:
    """
    Transforms the Traffic State dictionary into a flat numerical vector for DQN/PPO.
    """
    @staticmethod
    def build_state(traffic_state: Dict, current_phase: str, phase_elapsed: float, predicted_state: Dict = None) -> np.ndarray:
        lanes = traffic_state.get("lanes", {})
        
        # Aggregate NS vs EW
        ns_lanes = ["N1", "N2", "N3", "S1", "S2", "S3"]
        ew_lanes = ["E1", "E2", "E3", "W1", "W2", "W3"]
        
        ns_queue = sum(lanes.get(l, {}).get("queue_length", 0) for l in ns_lanes)
        ew_queue = sum(lanes.get(l, {}).get("queue_length", 0) for l in ew_lanes)
        
        # Phase encoding
        phase_enc = 1.0 if current_phase == "PHASE_1" else 0.0
        
        state_vec = [
            ns_queue,
            ew_queue,
            phase_enc,
            phase_elapsed
        ]
        
        if predicted_state:
            # Add simple forecast volumes
            pred_vol = predicted_state.get("t_plus_5", {}).get("vehicle_count", 0)
            state_vec.append(pred_vol)
            
        return np.array(state_vec, dtype=np.float32)
