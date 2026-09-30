class RLActionSpace:
    """
    Discrete actions the RL agent can propose.
    """
    ACTIONS = {
        0: {"action": "MAINTAIN", "phase": None, "reason": "RL_MAINTAIN"},
        1: {"action": "SWITCH_PHASE", "phase": "PHASE_1", "reason": "RL_SELECT_NS"},
        2: {"action": "SWITCH_PHASE", "phase": "PHASE_2", "reason": "RL_SELECT_EW"}
    }
    
    @staticmethod
    def decode(action_idx: int):
        return RLActionSpace.ACTIONS.get(action_idx, RLActionSpace.ACTIONS[0])
