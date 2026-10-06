import asyncio
import uuid
from datetime import datetime, timezone
import numpy as np

from backend.app.database.session import AsyncSessionLocal
from backend.app.models.traffic import TrafficState, TrafficStateEnum, SignalCommand, TrafficSignal
from backend.app.traffic.perception import Track
from backend.app.traffic.lane_logic import LaneManager, LaneConfig
from backend.app.traffic.speed import SpeedEstimator
from backend.app.traffic.state import TrafficStateAggregator
from backend.app.traffic.optimizer import TrafficOptimizer
from backend.app.safety.engine import SafetyEngine
from backend.app.traffic.controller import MockSignalController

async def run_pipeline_loop():
    print("Initializing MoviSabio Pipeline Runner...")
    
    # 1. Setup Environment
    lanes = [
        LaneConfig("N1", "Northbound", "Straight", [[0,0], [10,0], [10,10], [0,10]], 50.0),
        LaneConfig("S1", "Southbound", "Straight", [[10,0], [20,0], [20,10], [10,10]], 50.0),
        LaneConfig("E1", "Eastbound", "Straight", [[0,10], [10,10], [10,20], [0,20]], 50.0),
        LaneConfig("W1", "Westbound", "Straight", [[10,10], [20,10], [20,20], [10,20]], 50.0),
    ]
    lane_manager = LaneManager(lanes)
    speed_estimator = SpeedEstimator(calibration_matrix=None)
    state_aggregator = TrafficStateAggregator(lane_manager, speed_estimator)
    
    optimizer = TrafficOptimizer(mode="baseline")
    safety_engine = SafetyEngine({"min_green": 5.0, "max_green": 60.0})
    controller = MockSignalController()
    
    intersection_id = "INT-001"
    
    print("Starting continuous loop...")
    from backend.app.traffic.video import RTSPSource
    video_source = RTSPSource("rtsp://mock-camera")
    video_source.connect()
    
    while True:
        try:
            # 2. Mock CV Pipeline: Video -> YOLO -> Tracking
            frame = video_source.get_frame()
            # Generate fake tracks for demo purposes instead of real YOLO inference
            tracks = []
            for _ in range(np.random.randint(5, 30)):
                x = np.random.uniform(0, 20)
                y = np.random.uniform(0, 20)
                t = Track(str(uuid.uuid4()), 2, "car", [x-1, y-1, x+1, y+1], datetime.now(timezone.utc), "CAM-001")
                
                # Mock speed by updating position
                t.update([x-0.5, y-0.5, x+1.5, y+1.5], datetime.now(timezone.utc))
                tracks.append(t)
            
            # 3. Traffic State Aggregation
            state_dict = state_aggregator.aggregate(intersection_id, tracks)
            
            # 4. Save State to DB
            async with AsyncSessionLocal() as db:
                db_state = TrafficState(
                    intersection_id=intersection_id,
                    timestamp=datetime.fromisoformat(state_dict["timestamp"]),
                    vehicle_count=state_dict["vehicle_count"],
                    flow=state_dict["flow"],
                    average_speed=state_dict["average_speed"],
                    occupancy=state_dict["occupancy"],
                    queue_length=state_dict["queue_length"],
                    density=state_dict["density"],
                    congestion_level=TrafficStateEnum(state_dict["congestion_level"]),
                    lane_states=state_dict["lane_states"]
                )
                db.add(db_state)
                await db.commit()
            
            # 5. Optimizer
            current_signal_state = controller.get_state(intersection_id)
            recommendation = optimizer.optimize(state_dict, current_signal_state)
            
            # 6. Safety Engine
            safety_result = safety_engine.validate_command(current_signal_state, recommendation)
            
            # 7. Mock Signal Controller (HIL equivalent)
            if safety_result["status"] == "VALIDATED":
                recommendation["command_id"] = str(uuid.uuid4())
                success = controller.send_command(intersection_id, recommendation)
                
                # Save command to DB
                async with AsyncSessionLocal() as db:
                    cmd = SignalCommand(
                        command_id=recommendation["command_id"],
                        intersection_id=intersection_id,
                        signal_id=intersection_id,
                        requested_phase=recommendation["recommended_phase"],
                        duration=recommendation["duration"],
                        source="optimizer",
                        model_version="baseline",
                        policy_version="1.0",
                        safety_result="VALIDATED",
                        authorization="AUTO",
                        status="ACKNOWLEDGED" if success else "FAILED"
                    )
                    db.add(cmd)
                    await db.commit()
            
            print(f"[{datetime.now().isoformat()}] Pipeline Tick: {len(tracks)} tracks. Decision: {recommendation['recommended_phase']} (Safety: {safety_result['status']})")
            
        except Exception as e:
            print(f"Pipeline Error: {e}")
            
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run_pipeline_loop())
