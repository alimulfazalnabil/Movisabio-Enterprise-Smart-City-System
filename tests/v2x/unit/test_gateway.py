import pytest
from datetime import datetime, timezone, timedelta
from src.services.v2x.models.schemas import V2XMessage, TrustState
from src.services.v2x.engine.gateway import V2XGateway

def test_v2x_gateway_replay_protection():
    gateway = V2XGateway()
    
    now = datetime.now(timezone.utc)
    
    msg_fresh = V2XMessage(
        message_id="1", message_type="STATE", version="1.0", asset_id="A1",
        timestamp=now - timedelta(seconds=0.5), position={}, speed_mps=10, heading_deg=0, 
        source="V2V", quality="VALID", signature="valid_sig_A1"
    )
    
    msg_stale = V2XMessage(
        message_id="2", message_type="STATE", version="1.0", asset_id="A1",
        timestamp=now - timedelta(seconds=10.0), position={}, speed_mps=10, heading_deg=0, 
        source="V2V", quality="VALID", signature="valid_sig_A1"
    )
    
    msg_bad_sig = V2XMessage(
        message_id="3", message_type="STATE", version="1.0", asset_id="A1",
        timestamp=now - timedelta(seconds=0.5), position={}, speed_mps=10, heading_deg=0, 
        source="V2V", quality="VALID", signature="bad_sig"
    )
    
    assert gateway.validate_message(msg_fresh) == TrustState.TRUSTED
    assert gateway.validate_message(msg_stale) == TrustState.REJECTED
    assert gateway.validate_message(msg_bad_sig) == TrustState.REJECTED
