import time
from typing import Dict, Any

class CameraHealthMonitor:
    """
    Monitors RTSP stream health, FPS, and AI pipeline latency.
    """
    def __init__(self, camera_id: str):
        self.camera_id = camera_id
        self.status = "ONLINE"
        self.fps = 0.0
        self.inference_latency_ms = 0.0
        self.last_frame_time = time.time()
        
    def record_frame(self, inference_ms: float):
        now = time.time()
        self.fps = 1.0 / (now - self.last_frame_time) if (now - self.last_frame_time) > 0 else 0
        self.last_frame_time = now
        self.inference_latency_ms = inference_ms
        self.status = "ONLINE"
        
    def check_health(self) -> Dict[str, Any]:
        if time.time() - self.last_frame_time > 5.0:
            self.status = "OFFLINE"
            
        return {
            "camera_id": self.camera_id,
            "status": self.status,
            "fps": round(self.fps, 1),
            "inference_latency_ms": round(self.inference_latency_ms, 1)
        }
