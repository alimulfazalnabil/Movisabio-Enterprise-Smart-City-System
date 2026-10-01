import pytest
import asyncio
from src.services.ingestion.adapters.camera import RTSPCameraAdapter
from src.packages.events.schemas import CanonicalEvent, DataQuality

@pytest.mark.asyncio
async def test_camera_adapter_canonical_event():
    adapter = RTSPCameraAdapter("cam_01", "tenant_01", "rtsp://localhost")
    await adapter.connect()
    
    assert await adapter.health() == "healthy"
    
    # Receive one event
    async for event in adapter.receive():
        assert isinstance(event, CanonicalEvent)
        assert event.event_type == "camera.frame"
        assert event.tenant_id == "tenant_01"
        assert event.data_quality == DataQuality.VALID
        break # Only process one for testing
        
    await adapter.disconnect()
    assert await adapter.health() == "offline"
