import pytest
from datetime import datetime, timezone
from src.services.edge.models.schemas import EdgeEvent, ConnectivityState
from src.services.edge.engine.sync import StoreAndForwardSync

def test_store_and_forward():
    sync = StoreAndForwardSync()
    sync.set_connectivity(ConnectivityState.OFFLINE)
    
    event = EdgeEvent(
        event_id="e1",
        event_type="TRAFFIC_STATE",
        node_id="edge-1",
        payload={"queue": 10},
        occurred_at=datetime.now(timezone.utc),
        sync_status="PENDING"
    )
    
    sync.buffer_event(event)
    assert len(sync.local_event_store) == 1
    
    # Network recovers
    sync.set_connectivity(ConnectivityState.RECOVERING)
    
    # Buffer should be flushed
    assert len(sync.local_event_store) == 0
    assert event.sync_status == "SYNCED"

def test_sync_conflict_resolution():
    sync = StoreAndForwardSync()
    
    edge_state = {"plan": "LOCAL_EMERGENCY", "priority": 100}
    cloud_state = {"plan": "CLOUD_OPTIMIZED", "priority": 50}
    
    # Edge priority is higher (e.g. local safety override)
    resolved = sync.resolve_state_conflict(edge_state, cloud_state)
    assert resolved["plan"] == "LOCAL_EMERGENCY"
