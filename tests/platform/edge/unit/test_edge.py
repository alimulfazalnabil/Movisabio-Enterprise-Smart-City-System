from datetime import datetime, timezone, timedelta
import hashlib
from src.platform.edge.gateway import EdgeGateway, ConnectivityState
from src.platform.edge.autonomy import EdgeAutonomyEngine, AutonomyPolicy
from src.platform.synchronization.engine import SyncEngine, SyncRecord
from src.platform.mobile.evidence import MobileEvidence, Location
from src.platform.device_management.ota import OTARelease, OTADeployment

def test_edge_gateway_connectivity():
    now = datetime.now(timezone.utc)
    gateway = EdgeGateway(
        edge_site_id="site-1",
        tenant_id="tenant-1",
        connectivity_state=ConnectivityState.ONLINE,
        last_heartbeat=now - timedelta(seconds=40),
        software_version="1.0.0",
        configuration_version="v2"
    )
    
    gateway.evaluate_connectivity(now, timeout_seconds=30)
    assert gateway.connectivity_state == ConnectivityState.OFFLINE
    
    gateway.last_heartbeat = now - timedelta(seconds=20)
    gateway.evaluate_connectivity(now, timeout_seconds=30)
    assert gateway.connectivity_state == ConnectivityState.DEGRADED

def test_edge_autonomy():
    policy = AutonomyPolicy(
        policy_id="p1",
        allowed_actions=["apply_local_signal_plan", "store_video_locally"],
        max_autonomy_hours=4,
        fallback_mode="FLASHING_YELLOW"
    )
    engine = EdgeAutonomyEngine(policy)
    
    # Authorized under autonomy limits
    assert engine.can_execute_action("apply_local_signal_plan", offline_duration_hours=2.0) is True
    # Unauthorized action
    assert engine.can_execute_action("deploy_new_model", offline_duration_hours=2.0) is False
    # Exceeded duration
    assert engine.can_execute_action("apply_local_signal_plan", offline_duration_hours=5.0) is False

def test_sync_engine():
    engine = SyncEngine()
    record = SyncRecord(
        sync_id="sync-1",
        edge_site_id="site-1",
        object_type="INCIDENT",
        object_id="inc-1",
        direction="UPLOAD",
        object_version=1,
        source_timestamp=datetime.now(timezone.utc)
    )
    engine.enqueue(record)
    
    processed = engine.process_queue()
    assert len(processed) == 1
    assert processed[0].status == "SYNCHRONIZED"

def test_mobile_evidence():
    data = b"image_data_bytes"
    expected_hash = hashlib.sha256(data).hexdigest()
    
    evidence = MobileEvidence(
        evidence_id="ev-1",
        task_id="task-1",
        asset_id="asset-1",
        captured_at=datetime.now(timezone.utc),
        device_id="mobile-1",
        operator_id="user-1",
        location=Location(lat=10.0, lon=20.0),
        type="PHOTO",
        data_hash=expected_hash
    )
    
    assert evidence.verify_integrity(data) is True
    assert evidence.verify_integrity(b"tampered_data") is False

def test_ota_deployment():
    release = OTARelease(
        release_id="rel-1",
        component="edge_ai_model",
        version="2.0.0",
        signature="sig123"
    )
    
    deployment = OTADeployment(release, target_devices=["device-1"])
    
    # Should fail if not signed
    assert deployment.rollout() is False
    assert deployment.status == "FAILED_SIGNATURE"
    
    release.sign()
    assert deployment.rollout() is True
    assert deployment.status == "ROLLOUT"
