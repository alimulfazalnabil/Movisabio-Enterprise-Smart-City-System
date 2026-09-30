class RewardFunction:
    """
    Multi-objective reward for traffic signal optimization.
    """
    def __init__(self, w_queue=-1.0, w_delay=-0.5, w_switch=-2.0):
        self.w_queue = w_queue
        self.w_delay = w_delay
        self.w_switch = w_switch
        
    def calculate(self, previous_state, current_state, action_taken, safety_rejected):
        # Penalty for being rejected by safety layer
        if safety_rejected:
            return -10.0
            
        queue_penalty = current_state[0] + current_state[1] # ns_queue + ew_queue
        switch_penalty = 1.0 if action_taken != 0 else 0.0
        
        reward = (self.w_queue * queue_penalty) + (self.w_switch * switch_penalty)
        return reward
