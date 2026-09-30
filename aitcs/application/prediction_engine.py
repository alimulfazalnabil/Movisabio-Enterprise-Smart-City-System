"""PyTorch traffic forecasting model and its application-facing wrapper."""

from __future__ import annotations

import torch
import torch.nn as nn
from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass(frozen=True)
class PredictionResult:
    """Forecast for one intersection and one future time horizon."""

    intersection_id: str
    horizon_minutes: int
    predicted_congestion_index: float
    predicted_queue_length_meters: float
    predicted_arrival_count: int
    predicted_travel_time_seconds: float
    confidence_score: float

class TrafficLSTMModel(nn.Module):
    """LSTM network that maps a telemetry sequence to four traffic values."""

    def __init__(self, input_dim: int = 5, hidden_dim: int = 64, num_layers: int = 2, output_dim: int = 4):
        """Create an untrained network with the requested tensor dimensions."""

        super().__init__()
        self.lstm = nn.LSTM(input_size=input_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True, dropout=0.1)
        self.fc = nn.Sequential(nn.Linear(hidden_dim, 32), nn.ReLU(), nn.Linear(32, output_dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return the final-step projection for a ``(batch, time, input)`` tensor."""
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

class TrafficPredictionEngine:
    """Run the forecasting network and format its output at fixed horizons.

    The engine does not load trained weights. Callers must load a checkpoint
    into ``model`` before treating forecasts as operational predictions.
    """

    def __init__(self):
        """Select CPU/GPU, create the model and switch it to evaluation mode."""

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = TrafficLSTMModel().to(self.device)
        self.horizons = [1, 5, 10, 30]
        self.model.eval()

    @torch.no_grad()
    def predict_future_states(self, intersection_id: str, historical_tensor: np.ndarray) -> List[PredictionResult]:
        """Forecast traffic conditions from a sequence of five input features.

        Args:
            intersection_id: Identifier copied to every forecast.
            historical_tensor: Two-dimensional ``(time, 5)`` NumPy array.

        Returns:
            Forecasts for 1, 5, 10 and 30 minutes.

        Raises:
            RuntimeError: If the input shape is incompatible with the model.
        """
        self.model.eval()
        x = torch.tensor(historical_tensor, dtype=torch.float32).unsqueeze(0).to(self.device)
        raw_output = self.model(x).cpu().numpy().squeeze(0)
        
        base_congestion = float(np.clip(raw_output[0], 0.0, 1.0))
        base_queue = float(max(0.0, raw_output[1] * 250.0))
        base_arrivals = int(max(0, raw_output[2] * 100.0))
        base_travel_time = float(max(10.0, raw_output[3] * 120.0))

        results = []
        for i, horizon in enumerate(self.horizons):
            factor = 1.0 + (i * 0.05)
            results.append(PredictionResult(
                intersection_id=intersection_id,
                horizon_minutes=horizon,
                predicted_congestion_index=round(min(1.0, base_congestion * factor), 4),
                predicted_queue_length_meters=round(base_queue * factor, 2),
                predicted_arrival_count=int(base_arrivals * factor),
                predicted_travel_time_seconds=round(base_travel_time * factor, 2),
                confidence_score=round(max(0.5, 0.95 - (i * 0.1)), 2)
            ))
        return results
