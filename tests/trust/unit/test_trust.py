from src.services.trust.models.schemas import Identity, DataAsset, AccessRequest, DataTransferRequest
from src.services.trust.engine.authorization import AuthorizationEngine
from src.services.trust.engine.residency import ResidencyEngine

def test_authorization_evaluation():
    identity = Identity(
        identity_id="AGENT-01",
        identity_type="AI_AGENT",
        status="ACTIVE",
        attributes={"role": "TRAFFIC_OPTIMIZER"}
    )
    
    asset = DataAsset(
        asset_id="DATA-001",
        owner="MUNICIPALITY",
        classification="PERSONAL",
        jurisdiction="EU"
    )
    
    request_denied = AccessRequest(
        subject_id="AGENT-01",
        resource_id="DATA-001",
        action="read",
        purpose="GENERAL_RESEARCH"
    )
    
    engine = AuthorizationEngine()
    decision = engine.evaluate_access(request_denied, identity, asset)
    assert decision.decision == "DENY"

    request_allowed = AccessRequest(
        subject_id="AGENT-01",
        resource_id="DATA-001",
        action="read",
        purpose="EXPLICIT_CONSENT"
    )
    
    decision_allowed = engine.evaluate_access(request_allowed, identity, asset)
    assert decision_allowed.decision == "ALLOW"

def test_residency_evaluation():
    # Only allow EU -> EU or EU -> UK
    allowed = {
        "EU": ["UK"]
    }
    
    engine = ResidencyEngine(allowed_transfers=allowed)
    
    # Domestic
    req_domestic = DataTransferRequest(asset_id="DATA-01", source_jurisdiction="EU", target_jurisdiction="EU")
    assert engine.evaluate_transfer(req_domestic).decision == "ALLOW"
    
    # Allowed cross-border
    req_allowed = DataTransferRequest(asset_id="DATA-01", source_jurisdiction="EU", target_jurisdiction="UK")
    assert engine.evaluate_transfer(req_allowed).decision == "ALLOW"
    
    # Denied cross-border
    req_denied = DataTransferRequest(asset_id="DATA-01", source_jurisdiction="EU", target_jurisdiction="US")
    assert engine.evaluate_transfer(req_denied).decision == "DENY"
