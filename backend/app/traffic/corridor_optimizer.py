from typing import Dict, Any, List
import time

class CorridorOptimizer:
    """
    B8 - Multi-Intersection Corridor Intelligence
    Optimizes a corridor of connected intersections.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # B8.7 Corridor Objective Function Weights
        self.w_delay = config.get("w_delay", 1.0)
        self.w_queue = config.get("w_queue", 1.0)
        self.w_travel_time = config.get("w_travel_time", 1.0)
        self.w_stops = config.get("w_stops", 1.0)
        self.w_spillback = config.get("w_spillback", 5.0) # High penalty
        
        # B8.20 Oscillation Prevention
        self.min_decision_interval = config.get("min_decision_interval", 30.0)
        self.last_decision_times: Dict[str, float] = {}
        
    def detect_bottlenecks(self, intersection_states: Dict[str, Any]) -> Dict[str, float]:
        """B8.9 - Bottleneck Detection"""
        bottlenecks = {}
        for idx, state in intersection_states.items():
            inflow = state.get("arrival_flow", 0)
            discharge = state.get("departure_flow", 1) # Avoid div/0
            queue = state.get("queue_length", 0)
            
            # Simple bottleneck score formula
            score = (inflow / max(discharge, 0.1)) * (queue / 100.0)
            bottlenecks[idx] = min(score, 1.0)
        return bottlenecks

    def predict_spillback(self, upstream_idx: str, downstream_idx: str, states: Dict[str, Any]) -> float:
        """B8.8 - Spillback Prevention"""
        downstream = states.get(downstream_idx, {})
        upstream = states.get(upstream_idx, {})
        
        # If downstream queue is high and discharge is low, spillback risk is high
        ds_queue = downstream.get("queue_length", 0)
        capacity = downstream.get("capacity", 200) # Ex. meters
        
        risk = ds_queue / max(capacity, 1.0)
        return min(max(risk, 0.0), 1.0)

    def optimize_corridor(self, corridor_id: str, network_graph: Dict[str, Any], states: Dict[str, Any]) -> Dict[str, Any]:
        """B8.18 - Network-Level Optimization Loop"""
        current_time = time.time()
        
        bottlenecks = self.detect_bottlenecks(states)
        proposals = {}
        
        # Hierarchical Control: Compute global offsets/green-waves, then derive local commands
        for idx in network_graph["nodes"]:
            # B8.20 Prevent Oscillation
            last_time = self.last_decision_times.get(idx, 0)
            if current_time - last_time < self.min_decision_interval:
                continue # Cooldown active
                
            local_state = states.get(idx, {})
            # Look at downstream neighbor to prevent spillback
            downstream_neighbors = network_graph.get("edges", {}).get(idx, [])
            
            max_spillback = 0.0
            for neighbor in downstream_neighbors:
                risk = self.predict_spillback(idx, neighbor, states)
                max_spillback = max(max_spillback, risk)
                
            # If high spillback risk downstream, reduce green time or switch phase upstream
            if max_spillback > 0.8:
                proposals[idx] = {
                    "action": "THROTTLE",
                    "duration": 10.0,
                    "explanation": f"Spillback prevention (Risk: {max_spillback:.2f})"
                }
            else:
                # B8.5 Green-Wave Coordination - favor the corridor phase
                proposals[idx] = {
                    "action": "COORDINATED_GREEN",
                    "duration": 45.0,
                    "offset": 15.0, # B8.6 Offset Optimization
                    "explanation": f"Green-wave offset, Bottleneck score: {bottlenecks.get(idx, 0):.2f}"
                }
                
            self.last_decision_times[idx] = current_time
            
        return proposals
