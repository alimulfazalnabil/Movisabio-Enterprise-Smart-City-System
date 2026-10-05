from datetime import datetime, timezone
from src.platform.mlops.registry.models import MLModel, MLModelVersion
from src.platform.mlops.governance.approval import ModelApprovalWorkflow
from src.platform.mlops.monitoring.drift import DriftDetector

def test_model_approval_r3():
    model = MLModel(
        model_id="traffic-forecast",
        name="Traffic Volume Forecaster",
        domain="traffic",
        model_type="LSTM",
        risk_class="R3"
    )
    
    version = MLModelVersion(
        version_id="v1.0",
        model_id="traffic-forecast",
        version="1.0",
        artifact_uri="s3://models/traffic/1.0",
        status="EVALUATED",
        created_at=datetime.now(timezone.utc)
    )
    
    # R3 model should be approvable
    assert ModelApprovalWorkflow.approve_model(model, version) == True
    assert version.status == "APPROVED"

def test_model_approval_r5_requires_signature():
    model = MLModel(
        model_id="traffic-control-rl",
        name="Traffic RL Controller",
        domain="traffic",
        model_type="PPO",
        risk_class="R5"
    )
    
    version_no_sig = MLModelVersion(
        version_id="v1.0",
        model_id="traffic-control-rl",
        version="1.0",
        artifact_uri="s3://models/traffic/rl/1.0",
        status="EVALUATED",
        created_at=datetime.now(timezone.utc)
    )
    
    # R5 without signature should fail
    assert ModelApprovalWorkflow.approve_model(model, version_no_sig) == False
    assert version_no_sig.status == "EVALUATED"
    
    version_with_sig = MLModelVersion(
        version_id="v1.1",
        model_id="traffic-control-rl",
        version="1.1",
        artifact_uri="s3://models/traffic/rl/1.1",
        status="EVALUATED",
        signature="sig-hash-12345",
        created_at=datetime.now(timezone.utc)
    )
    
    # R5 with signature should pass
    assert ModelApprovalWorkflow.approve_model(model, version_with_sig) == True
    assert version_with_sig.status == "APPROVED"

def test_drift_detection():
    baseline = [10.0, 11.0, 9.0, 10.5]
    
    # Healthy (similar distribution)
    healthy = [10.2, 10.8, 9.5, 10.1]
    assert DriftDetector.detect_drift(baseline, healthy) == "HEALTHY"
    
    # Warning (shifted but not catastrophic)
    warning = [16.0, 15.0, 17.0, 16.5]
    assert DriftDetector.detect_drift(baseline, warning) == "WARNING"
    
    # Degraded (major shift)
    degraded = [25.0, 26.0, 24.0, 25.5]
    assert DriftDetector.detect_drift(baseline, degraded) == "DEGRADED"
