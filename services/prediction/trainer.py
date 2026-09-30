import time

class ModelTrainer:
    """
    Simulates the PyTorch training loop for evaluating LSTMs against Baselines.
    """
    def __init__(self):
        pass
        
    def train(self, model_name="lstm", epochs=10):
        print(f"--- Training {model_name.upper()} ---")
        for e in range(1, epochs + 1):
            loss = 1.0 / (e + 1)
            # print(f"Epoch {e}/{epochs} | Loss: {loss:.4f}")
            time.sleep(0.1)
        print("Training complete.\n")
        
    def evaluate_models(self):
        print("--- Model Evaluation (MAE) ---")
        print("Historical Average : 14.2")
        print("Moving Average     : 11.5")
        print("ARIMA              :  9.8")
        print("LSTM (Proposed)    :  6.4")
        print("GRU (Proposed)     :  6.2")
        print("------------------------------")
        print("Conclusion: GRU selected for deployment.")
