import pandas as pd
import numpy as np

class FeatureEngineer:
    """
    Transforms raw traffic state sequences into predictive features.
    """
    def __init__(self):
        self.history = []
        
    def add_state(self, state_snapshot: dict):
        self.history.append(state_snapshot)
        if len(self.history) > 60:  # Keep 1 hour of 1-minute aggregations
            self.history.pop(0)
            
    def build_features(self) -> np.ndarray:
        """
        Creates a time-series feature matrix (num_steps, num_features).
        Features: [vehicle_count, avg_speed, queue_length] per lane.
        """
        # Mock feature generation for current history
        if not self.history:
            return np.zeros((12, 3))
            
        features = []
        for state in self.history[-12:]: # Last 12 steps
            lanes = state.get("lanes", {})
            total_vol = sum([l.get("vehicle_count", 0) for l in lanes.values()])
            avg_spd = np.mean([l.get("average_speed", 0) for l in lanes.values()]) if lanes else 0
            tot_q = sum([l.get("queue_length", 0) for l in lanes.values()])
            features.append([total_vol, avg_spd, tot_q])
            
        # Pad if needed
        while len(features) < 12:
            features.insert(0, [0.0, 0.0, 0.0])
            
        return np.array(features)
