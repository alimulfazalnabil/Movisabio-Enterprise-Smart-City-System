from simulation.rl.state import RLStateBuilder
from simulation.rl.actions import RLActionSpace
from simulation.rl.reward import RewardFunction

class SumoRLEnvironment:
    """
    Gym-like wrapper for SUMO TraCI and MoviSabio traffic state.
    """
    def __init__(self, traci_client, controller, state_engine):
        self.traci = traci_client
        self.controller = controller
        self.state_engine = state_engine
        self.reward_fn = RewardFunction()
        self.current_state_vec = None
        
    def reset(self):
        # In a real environment, this restarts the SUMO simulation
        self.current_state_vec = RLStateBuilder.build_state({"lanes": {}}, "PHASE_1", 0.0)
        return self.current_state_vec
        
    def step(self, action_idx: int):
        decoded = RLActionSpace.decode(action_idx)
        
        # Pass RL action to safety layer
        audit = self.controller.request_action(
            requested_action=decoded["action"],
            requested_phase=decoded["phase"] if decoded["phase"] else self.controller.get_state()["phase"],
            reason=decoded["reason"],
            optimizer="RL-Agent"
        )
        
        safety_rejected = audit["safety_status"] == "REJECTED"
        
        # Advance simulation
        self.traci.advance()
        
        # Observe new state
        raw_detections = self.traci.get_vehicle_state("INT-001")
        traffic_state = self.state_engine.update("INT-001", raw_detections)
        new_signal = self.controller.get_state()
        
        next_state_vec = RLStateBuilder.build_state(traffic_state, new_signal["phase"], new_signal["elapsed"])
        
        # Calculate Reward
        reward = self.reward_fn.calculate(self.current_state_vec, next_state_vec, action_idx, safety_rejected)
        
        self.current_state_vec = next_state_vec
        done = False # Depends on episode length
        
        return next_state_vec, reward, done, audit
