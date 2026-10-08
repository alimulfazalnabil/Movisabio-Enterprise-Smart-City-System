"""Production-safe traffic forecasting boundary.

The ML model is never treated as operational until a versioned checkpoint is
explicitly loaded. When no trained checkpoint is available, the engine exposes
an honest persistence baseline so the rest of the AITCS pipeline can still be
demonstrated without fabricating model output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import hashlib
import numpy as np
import torch
import torch.nn as nn


FEATURE_ORDER = (
    "vehicle_count",
    "occupancy_percentage",
    "queue_length_meters",
    "average_speed_kmh",
    "congestion_index",
)
HORIZONS_MINUTES = (1, 5, 10, 30)


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
    evidence_class: str = "PREDICTED"
    model_id: str = "persistence-baseline"
    model_version: str = "1.0.0"
    quality: str = "VALID"
    correlation_id: Optional[str] = None


class TrafficLSTMModel(nn.Module):
    """LSTM network mapping a telemetry sequence to four traffic outputs."""

    def __init__(self, input_dim: int = 5, hidden_dim: int = 64, num_layers: int = 2, output_dim: int = 4):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.1 if num_layers > 1 else 0.0,
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])


class TrafficPredictionEngine:
    """Forecast traffic with an explicit ML/baseline operating mode.

    The default mode is a persistence baseline. It is deterministic and is
    clearly marked as a predicted baseline rather than an empirical ML model.
    ML mode requires a real checkpoint and refuses to run without one.
    """

    def __init__(
        self,
        checkpoint_path: str | None = None,
        model_id: str = "traffic-lstm",
        model_version: str = "unloaded",
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = TrafficLSTMModel().to(self.device)
        self.horizons = list(HORIZONS_MINUTES)
        self.model_id = model_id
        self.model_version = model_version
        self.checkpoint_sha256: Optional[str] = None
        self.ml_ready = False
        self.model.eval()

        if checkpoint_path:
            self.load_checkpoint(checkpoint_path)

    def load_checkpoint(self, checkpoint_path: str) -> None:
        """Load a versioned PyTorch checkpoint and mark ML inference ready."""
        import pathlib

        path = pathlib.Path(checkpoint_path)
        if not path.is_file():
            raise FileNotFoundError(f"Prediction checkpoint not found: {path}")

        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checkpoint = torch.load(path, map_location=self.device)

        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
            self.model_version = str(checkpoint.get("model_version", self.model_version))
            self.model_id = str(checkpoint.get("model_id", self.model_id))
        else:
            state_dict = checkpoint

        self.model.load_state_dict(state_dict)
        self.model.eval()
        self.checkpoint_sha256 = digest
        self.ml_ready = True

    def _validate_history(self, historical_tensor: np.ndarray) -> np.ndarray:
        x = np.asarray(historical_tensor, dtype=np.float32)
        if x.ndim != 2 or x.shape[1] != len(FEATURE_ORDER):
            raise ValueError(
                f"historical_tensor must have shape (time, {len(FEATURE_ORDER)}) "
                f"with feature order {FEATURE_ORDER}; got {x.shape}"
            )
        if x.shape[0] < 1:
            raise ValueError("historical_tensor must contain at least one observation")
        if not np.isfinite(x).all():
            raise ValueError("historical_tensor contains NaN or infinite values")
        return x

    @staticmethod
    def _baseline(history: np.ndarray, horizon: int) -> PredictionResult:
        last = history[-1]
        vehicle_count = max(0, int(round(float(last[0]))))
        occupancy = float(np.clip(last[1], 0.0, 100.0))
        queue = max(0.0, float(last[2]))
        speed = max(0.1, float(last[3]))
        congestion = float(np.clip(last[4], 0.0, 1.0))
        travel_time = (0.5 / speed) * 3600.0

        return PredictionResult(
            intersection_id="",
            horizon_minutes=horizon,
            predicted_congestion_index=round(congestion, 4),
            predicted_queue_length_meters=round(queue, 2),
            predicted_arrival_count=vehicle_count,
            predicted_travel_time_seconds=round(travel_time, 2),
            confidence_score=0.0,
            evidence_class="PREDICTED_BASELINE",
            model_id="persistence-baseline",
            model_version="1.0.0",
            quality="VALID",
        )

    @torch.no_grad()
    def predict_future_states(
        self,
        intersection_id: str,
        historical_tensor: np.ndarray,
        *,
        correlation_id: str | None = None,
        require_ml: bool = False,
    ) -> List[PredictionResult]:
        """Forecast at 1/5/10/30 minutes with explicit provenance."""
        history = self._validate_history(historical_tensor)

        if require_ml and not self.ml_ready:
            raise RuntimeError(
                "Operational ML prediction requested but no trained checkpoint is loaded."
            )

        if not self.ml_ready:
            return [
                PredictionResult(
                    **{
                        **self._baseline(history, horizon).__dict__,
                        "intersection_id": intersection_id,
                        "correlation_id": correlation_id,
                    }
                )
                for horizon in self.horizons
            ]

        x = torch.tensor(history, dtype=torch.float32).unsqueeze(0).to(self.device)
        raw = self.model(x).cpu().numpy().reshape(-1)

        base = {
            "predicted_congestion_index": float(np.clip(raw[0], 0.0, 1.0)),
            "predicted_queue_length_meters": float(max(0.0, raw[1])),
            "predicted_arrival_count": max(0, int(round(raw[2]))),
            "predicted_travel_time_seconds": float(max(0.1, raw[3])),
        }

        return [
            PredictionResult(
                intersection_id=intersection_id,
                horizon_minutes=horizon,
                **{k: round(v, 4) if isinstance(v, float) else v for k, v in base.items()},
                confidence_score=0.0,
                evidence_class="PREDICTED",
                model_id=self.model_id,
                model_version=self.model_version,
                quality="VALID",
                correlation_id=correlation_id,
            )
            for horizon in self.horizons
        ]
