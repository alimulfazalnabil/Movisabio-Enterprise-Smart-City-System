from pydantic import BaseModel
import datetime

class PredictionOutput(BaseModel):
    model_id: str
    model_version: str
    prediction_timestamp: datetime.datetime
    predicted_congestion_index: float

class BaselinePredictionEngine:
    def __init__(self):
        self.model_id = "baseline_ewma"
        self.version = "1.0.0"
        self.alpha = 0.3
        self.previous_congestion = 0.0

    def predict_next_step(self, current_congestion: float) -> PredictionOutput:
        """
        Uses an Exponentially Weighted Moving Average (EWMA) as a robust baseline
        before introducing neural networks.
        """
        predicted = (self.alpha * current_congestion) + ((1 - self.alpha) * self.previous_congestion)
        self.previous_congestion = current_congestion
        
        return PredictionOutput(
            model_id=self.model_id,
            model_version=self.version,
            prediction_timestamp=datetime.datetime.now(datetime.timezone.utc),
            predicted_congestion_index=predicted
        )
