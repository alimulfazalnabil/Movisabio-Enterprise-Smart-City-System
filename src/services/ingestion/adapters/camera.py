from typing import AsyncGenerator
from datetime import datetime, timezone
from src.services.ingestion.adapters.base import DataSourceAdapter
from src.packages.events.schemas import CanonicalEvent, SourceRef, DataQuality
import asyncio

class RTSPCameraAdapter(DataSourceAdapter):
    """
    Simulates connecting to an RTSP stream and bridging frames to the processing engine.
    In actual implementation, this spawns an ffmpeg or OpenCV capture thread.
    """
    
    def __init__(self, camera_id: str, tenant_id: str, rtsp_url: str):
        self.camera_id = camera_id
        self.tenant_id = tenant_id
        self.rtsp_url = rtsp_url
        self._connected = False
        
    async def connect(self) -> bool:
        # Mock connection to RTSP
        self._connected = True
        return True
        
    async def health(self) -> str:
        return "healthy" if self._connected else "offline"

    async def receive(self) -> AsyncGenerator[CanonicalEvent, None]:
        # In a real environment, this yields camera.frame events containing raw bytes
        # or metadata emitted by edge CV processes.
        while self._connected:
            await asyncio.sleep(0.1) # Simulate 10 FPS
            
            now = datetime.now(timezone.utc)
            yield CanonicalEvent(
                event_type="camera.frame",
                event_version="1.0",
                tenant_id=self.tenant_id,
                source=SourceRef(type="camera", id=self.camera_id),
                event_time=now,
                ingestion_time=now,
                data_quality=DataQuality.VALID,
                payload={
                    "resolution": "1920x1080",
                    "format": "h264",
                    # "frame_bytes": b"..."  (In practice, large binary data goes to S3/Redis, not JSON bus)
                }
            )

    async def disconnect(self) -> None:
        self._connected = False
