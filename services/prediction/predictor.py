from services.prediction.baseline import BaselinePredictor
from services.prediction.models import LSTMPredictor, GRUPredictor
from services.prediction.feature_engineering import FeatureEngineer
import numpy as np

class TrafficPredictor:
    """
    Unified Prediction API. Consumes real-time traffic state, engineers features,
    and queries the active model (Baseline/LSTM/GRU) for the t+5, t+10, t+15 forecast.
    """
    def __init__(self, active_model="lstm"):
        self.fe = FeatureEngineer()
        
        if active_model == "baseline":
            self.model = BaselinePredictor()
        elif active_model == "lstm":
            self.model = LSTMPredictor()
        elif active_model == "gru":
            self.model = GRUPredictor()
        else:
            raise ValueError("Unknown model type")
            
    def update_and_predict(self, current_traffic_state: dict) -> dict:
        # 1. Store and transform
        self.fe.add_state(current_traffic_state)
        features = self.fe.build_features()
        
        # 2. Predict next 3 steps (15 mins)
        forecast_array = self.model.predict(features)
        
        # 3. Format as standard JSON schema
        return {
            "t_plus_5": {
                "vehicle_count": int(forecast_array[0][0]),
                "average_speed": float(forecast_array[0][1]),
                "queue_length": int(forecast_array[0][2])
            },
            "t_plus_10": {
                "vehicle_count": int(forecast_array[1][0]),
                "average_speed": float(forecast_array[1][1]),
                "queue_length": int(forecast_array[1][2])
            },
            "t_plus_15": {
                "vehicle_count": int(forecast_array[2][0]),
                "average_speed": float(forecast_array[2][1]),
                "queue_length": int(forecast_array[2][2])
            }
        }
