"""Experimental DQN components for traffic-signal action selection."""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class RLAgentDecision:
    """Selected discrete action and the values used to choose it."""

    intersection_id: str
    selected_action: int
    q_values: List[float]
    reward_estimate: float
    exploration_rate: float

class TrafficQNetwork(nn.Module):
    """Feed-forward network that estimates a value for each signal action."""

    def __init__(self, state_dim: int = 12, action_dim: int = 4, hidden_dim: int = 128):
        """Create an untrained Q-network for fixed-size state vectors."""

        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return one Q-value per action for each input state."""
        return self.net(x)

class ReinforcementLearningEngine:
    """Select actions with an epsilon-greedy, currently untrained policy."""

    def __init__(self, state_dim: int = 12, action_dim: int = 4, lr: float = 0.001, gamma: float = 0.99):
        """Create policy/target networks and an optimizer on CPU or GPU."""

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        
        self.policy_net = TrafficQNetwork(state_dim, action_dim).to(self.device)
        self.target_net = TrafficQNetwork(state_dim, action_dim).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.epsilon = 0.1

    def select_action(self, intersection_id: str, state_vector: np.ndarray) -> RLAgentDecision:
        """Choose an action for a one-dimensional state vector.

        Returns either a random exploratory action or the policy's highest-value
        action, together with diagnostic values. This method does not train the
        network.
        """
        self.policy_net.eval()
        if np.random.rand() < self.epsilon:
            action = np.random.randint(0, self.action_dim)
            q_values = [0.0] * self.action_dim
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(state_vector, dtype=torch.float32).unsqueeze(0).to(self.device)
                q_tensor = self.policy_net(state_tensor)
                q_values = q_tensor.cpu().numpy().squeeze(0).tolist()
                action = int(torch.argmax(q_tensor).item())

        estimated_reward = -float(state_vector[0] * 0.5 + state_vector[1] * 0.3)
        return RLAgentDecision(intersection_id, action, q_values, round(estimated_reward, 2), self.epsilon)

    def compute_reward(self, delay: float, queue_length: float, stops: int, emissions: float, throughput: int) -> float:
        """Score throughput against delay, queues, stops and emissions."""
        penalty = (0.3 * delay) + (0.3 * queue_length) + (0.1 * stops) + (0.1 * emissions)
        bonus = 0.2 * throughput
        return round(float(bonus - penalty), 4)
