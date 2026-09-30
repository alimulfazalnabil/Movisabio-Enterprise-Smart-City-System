from ml.registry.manager import MLModelRegistry, ModelManager
import datetime

def simulate_training_run(manager: ModelManager):
    """
    Phase 10: ML Training Simulator
    Demonstrates training a model and registering it.
    """
    print("Training YOLOv10 on intersection datasets...")
    
    # Mock training metrics
    metrics = {
        "mAP_50": 0.95,
        "mAP_50_95": 0.78,
        "inference_ms": 12.5
    }
    
    new_model = MLModelRegistry(
        model_id="yolo_perception_core",
        version="v1.0.4",
        architecture="YOLOv10",
        deployment_status="SHADOW",
        training_date=datetime.datetime.now(datetime.timezone.utc),
        metrics=metrics,
        weights_uri="s3://movisabio-models/yolo_perception_core/v1.0.4/best.pt"
    )
    
    manager.register_model(new_model)
    print(f"Registered model {new_model.model_id}:{new_model.version} in SHADOW mode.")
