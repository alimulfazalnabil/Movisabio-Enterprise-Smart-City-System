class BaselinePredictor:
    """
    Non-neural baselines (Moving Average, Historical Average) to validate
    whether deep learning models actually provide lift.
    """
    def __init__(self, method="moving_average"):
        self.method = method
        
    def predict(self, feature_sequence):
        """
        Expects shape (steps, features). 
        Returns next 3 steps of [vehicle_count, avg_speed, queue_length].
        """
        if self.method == "moving_average":
            # Simple moving average of last 3 steps
            recent = feature_sequence[-3:]
            avg = recent.mean(axis=0)
            # Forecast flat for next 3 steps
            return [avg, avg, avg]
        else:
            # Fallback to zero (or historical average if we had a DB)
            return [[0,0,0], [0,0,0], [0,0,0]]
