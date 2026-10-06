class TrafficOptimizer:
    def __init__(self, mode: str = "baseline"):
        self.mode = mode

    def optimize(self, traffic_state: dict, signal_state: dict) -> dict:
        if self.mode == "baseline":
            return self._baseline_policy(traffic_state, signal_state)
        else:
            return self._rl_policy(traffic_state, signal_state)

    def _baseline_policy(self, traffic_state: dict, signal_state: dict) -> dict:
        # Simple deterministic queue-based logic
        ns_queue = 0
        ew_queue = 0
        
        for lane_id, lane_data in traffic_state.get("lane_states", {}).items():
            if "N" in lane_id or "S" in lane_id:
                ns_queue += lane_data.get("current_vehicle_count", 0)
            elif "E" in lane_id or "W" in lane_id:
                ew_queue += lane_data.get("current_vehicle_count", 0)
                
        current_phase = signal_state.get("phase", "NS_GREEN")
        
        if ns_queue > ew_queue:
            recommended = "NS_GREEN"
        elif ew_queue > ns_queue:
            recommended = "EW_GREEN"
        else:
            recommended = current_phase
            
        return {
            "recommended_phase": recommended,
            "duration": 30.0 if recommended != current_phase else signal_state.get("remaining", 30.0),
            "expected_delay": 15.0,
            "expected_queue": max(ns_queue, ew_queue),
            "expected_throughput": 1200.0,
            "confidence": 0.85,
            "explanation": f"NS={ns_queue}, EW={ew_queue}",
            "counterfactual_baseline": {
                "expected_delay_without_intervention": 25.0,
                "expected_queue_without_intervention": max(ns_queue, ew_queue) + 10
            }
        }

    def _rl_policy(self, traffic_state: dict, signal_state: dict) -> dict:
        # RL placeholder
        return {
            "recommended_phase": "NS_GREEN",
            "duration": 30.0,
            "expected_delay": 10.0,
            "expected_queue": 5,
            "expected_throughput": 1500.0,
            "confidence": 0.95,
            "explanation": "RL_PPO",
            "counterfactual_baseline": {
                "expected_delay_without_intervention": 25.0,
                "expected_queue_without_intervention": 20
            }
        }
