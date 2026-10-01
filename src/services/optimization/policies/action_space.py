from enum import IntEnum

class OptimizerAction(IntEnum):
    """
    Constrained Action Space for the RL Agent.
    The agent outputs integer indices which map to these semantic intents.
    """
    HOLD = 0
    EXTEND_5 = 1
    EXTEND_10 = 2
    TERMINATE = 3
    SELECT_NEXT = 4
