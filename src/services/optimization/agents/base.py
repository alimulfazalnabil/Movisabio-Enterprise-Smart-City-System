from abc import ABC, abstractmethod
from typing import Dict, Any, List

from src.services.optimization.state.models import OptimizationState
from src.services.optimization.decisions.models import OptimizationDecision

class OptimizationAgent(ABC):
    """
    Abstract Base Class for optimization strategies (Baseline, DQN, PPO, etc.).
    """
    
    def __init__(self, agent_id: str, version: str):
        self.agent_id = agent_id
        self.version = version
        
    @abstractmethod
    def evaluate(self, state: OptimizationState, valid_actions: List[bool]) -> OptimizationDecision:
        """
        Evaluate the normalized state and return a Candidate OptimizationDecision.
        Must only select actions where valid_actions is True.
        """
        pass
        
    @abstractmethod
    def train(self, batch: Any) -> Dict[str, float]:
        """
        Train the model on a batch of experience.
        Returns training metrics (loss, etc.).
        """
        pass
