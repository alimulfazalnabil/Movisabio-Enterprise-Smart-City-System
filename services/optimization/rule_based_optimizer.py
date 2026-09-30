from typing import Dict, Any

class RuleBasedOptimizer:
    """
    Deterministically evaluates traffic state and proposes signal actions.
    No RL, no black box. Just clear, explainable logic.
    """
    def __init__(self):
        self.version = "rule-based-v1"
        
    def evaluate(self, traffic_state: Dict[str, Any], current_signal_state: Dict[str, Any], forecast: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Example Logic:
        If E/W queue > N/S queue + 5, request Phase 2 (E/W Green).
        Else if N/S queue > E/W queue + 5, request Phase 1 (N/S Green).
        If forecast shows E/W demand surging in 5 mins, prioritize Phase 2.
        Otherwise, maintain current phase.
        """
        lanes = traffic_state.get("lanes", {})
        
        # Aggregate queues
        ns_queue = sum([lanes.get(l, {}).get("queue_length", 0) for l in ["N1", "N2", "N3", "S1", "S2", "S3"]])
        ew_queue = sum([lanes.get(l, {}).get("queue_length", 0) for l in ["E1", "E2", "E3", "W1", "W2", "W3"]])
        
        current_phase = current_signal_state.get("phase", "PHASE_1")
        
        requested_phase = current_phase
        reason = "MAINTAIN_BALANCE"
        action = "MAINTAIN"
        
        # Factor in forecast if available
        if forecast:
            predicted_vol = forecast.get("t_plus_5", {}).get("vehicle_count", 0)
            if predicted_vol > 50 and current_phase == "PHASE_1": # Just a mock logic to use forecast
                return {
                    "requested_action": "SWITCH_PHASE",
                    "requested_phase": "PHASE_2",
                    "reason": "ANTICIPATE_SURGE",
                    "optimizer": self.version + "-predictive"
                }
        
        if ew_queue > ns_queue + 5 and current_phase == "PHASE_1":
            requested_phase = "PHASE_2"
            reason = "HIGH_EW_QUEUE"
            action = "SWITCH_PHASE"
        elif ns_queue > ew_queue + 5 and current_phase == "PHASE_2":
            requested_phase = "PHASE_1"
            reason = "HIGH_NS_QUEUE"
            action = "SWITCH_PHASE"
            
        return {
            "requested_action": action,
            "requested_phase": requested_phase,
            "reason": reason,
            "optimizer": self.version
        }
