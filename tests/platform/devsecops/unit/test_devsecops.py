import pytest
from datetime import datetime, timezone
from src.platform.devsecops.pipeline.gates import QualityGate, SecurityGate
from src.platform.devsecops.registry.artifacts import Artifact, ArtifactRegistry
from src.platform.devsecops.deployment.strategy import DeploymentController

def test_quality_gate():
    tests = {"unit": True, "integration": True}
    security = {"sast": True, "sca": True}
    assert QualityGate.evaluate(tests, security) is True
    
    security["sast"] = False
    assert QualityGate.evaluate(tests, security) is False

def test_security_gate_secrets():
    safe_commits = ["fix: bug in router", "feat: add new endpoint"]
    unsafe_commits = ["fix: bug", "chore: update api_key=12345"]
    
    assert SecurityGate.scan_secrets(safe_commits) is True
    assert SecurityGate.scan_secrets(unsafe_commits) is False

def test_deployment_approval_gate():
    registry = ArtifactRegistry()
    artifact = Artifact(
        artifact_id="art-1",
        digest="sha256:123",
        version="v1",
        commit_sha="abc",
        sbom_uri="s3://sboms/art-1",
        created_at=datetime.now(timezone.utc)
    )
    registry.register(artifact)
    
    controller = DeploymentController()
    
    # Try to deploy to PROD without approval
    deploy = controller.create_deployment(artifact, "PRODUCTION")
    success = deploy.progress_rollout(10)
    assert success is False
    assert deploy.status == "BLOCKED_UNAPPROVED"
    
    # Approve and retry
    registry.approve(artifact.artifact_id)
    success = deploy.progress_rollout(10)
    assert success is True
    assert deploy.status == "IN_PROGRESS"
    
    # Rollback
    deploy.rollback()
    assert deploy.status == "ROLLED_BACK"
    assert deploy.rollout_percentage == 0
