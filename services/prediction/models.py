import numpy as np

class MockNeuralNet:
    """
    Simulates an LSTM/GRU predicting higher future traffic if a trend is rising.
    In real implementation, this wraps PyTorch/TensorFlow models.
    """
    def __init__(self, architecture="LSTM"):
        self.architecture = architecture
        
    def predict(self, feature_sequence: np.ndarray) -> np.ndarray:
        # feature_sequence shape: (12, 3) -> [vol, speed, queue]
        
        # Simple heuristic to mock "intelligence"
        # If queue is growing in the last 3 steps, forecast aggressive growth
        recent_queues = feature_sequence[-3:, 2]
        is_growing = recent_queues[2] > recent_queues[0]
        
        last_step = feature_sequence[-1]
        
        forecast = []
        current = last_step.copy()
        
        for i in range(3):
            if is_growing:
                current[0] *= 1.1 # Vol increases
                current[1] *= 0.9 # Speed decreases
                current[2] += 5.0 # Queue increases
            else:
                current[0] *= 0.95 
                current[1] *= 1.05
                current[2] = max(0, current[2] - 2)
            forecast.append(current.copy())
            
        return np.array(forecast)
        
class LSTMPredictor(MockNeuralNet):
    def __init__(self):
        super().__init__("LSTM")
        
class GRUPredictor(MockNeuralNet):
    def __init__(self):
        super().__init__("GRU")
