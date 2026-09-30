from fastapi import APIRouter, Depends, UploadFile, File
import datetime

from security.auth import require_permission
from security.rbac import Permission, Role
from services.perception.pipeline import PerceptionPipeline

router = APIRouter(prefix="/api/v1/perception", tags=["Perception & CV"])

# Initialize the pipeline globally or inject it
perception_pipeline = PerceptionPipeline()

@router.post("/process-frame")
async def process_rtsp_frame(
    intersection_id: str,
    camera_id: str,
    frame: UploadFile = File(...),
    # Require specific service account permission to submit frames
    role: Role = Depends(require_permission(Permission.CONTROL_SIGNAL)) # Just an example permission
):
    """
    Ingests an RTSP video frame and runs the complete perception pipeline:
    YOLO -> ByteTrack -> Lane Association -> Speed Estimation.
    """
    frame_bytes = await frame.read()
    
    # 1. Process through perception pipeline
    tracked_objects = perception_pipeline.process_frame(
        frame=frame_bytes,
        intersection_id=intersection_id,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    # 2. Compute Traffic State
    from services.traffic_state.engine import TrafficStateEngine
    traffic_state_engine = TrafficStateEngine()
    state_output = traffic_state_engine.compute_state(intersection_id, tracked_objects)
    
    # 3. Predict Future State
    from services.prediction.baseline import BaselinePredictionEngine
    prediction_engine = BaselinePredictionEngine()
    prediction = prediction_engine.predict_next_step(state_output.congestion_index)
    
    # 4. Optimization Engine Decision
    from services.optimization.rule_based import OptimizationEngine
    optimizer = OptimizationEngine()
    decision = optimizer.compute_decision(state_output)
    
    # 5. Safety Engine Validation
    from services.safety.engine import SafetyEngine
    safety = SafetyEngine()
    current_intersection_mock_state = {"conflicting_phase": "RED"} # Mocked
    safety_result = safety.validate_decision(decision, current_intersection_mock_state)
    
    # 6. Command Outbox & Actuation
    from services.actuation.outbox import CommandOutbox
    outbox = CommandOutbox()
    
    final_command = None
    if safety_result.is_safe:
        final_command = outbox.create_command(
            intersection_id=intersection_id,
            phase=decision.desired_phase,
            requested_state=safety_result.permitted_state,
            reason=safety_result.reason
        )
        # Normally this would be picked up by a background worker/Kafka consumer to send to the Controller.
    
    return {
        "status": "success",
        "intersection_id": intersection_id,
        "traffic_state": state_output.model_dump(),
        "prediction": prediction.model_dump(),
        "safety_result": safety_result.model_dump(),
        "dispatched_command": final_command.model_dump() if final_command else None
    }
