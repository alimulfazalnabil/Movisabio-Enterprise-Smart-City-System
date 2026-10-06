from src.platform.global_platform.regions.registry import Region, RegionRegistry
from src.platform.global_platform.sovereignty.residency import ResidencyPolicy, DataTransferRequest, TransferEngine
from src.platform.global_platform.discovery.services import ServiceEndpoint, GlobalServiceRegistry

def test_region_health():
    registry = RegionRegistry()
    region = Region(region_id="eu-de-01", region_code="DE", jurisdiction_id="DE", provider="aws")
    registry.register(region)
    
    assert registry.get_region("eu-de-01").status == "HEALTHY"
    
    registry.update_health("eu-de-01", "DEGRADED")
    assert registry.get_region("eu-de-01").status == "DEGRADED"

def test_data_transfer_engine():
    engine = TransferEngine()
    policy = ResidencyPolicy(
        tenant_id="tenant-1",
        data_classification="SENSITIVE",
        primary_region="eu-de-01",
        allowed_regions=["eu-de-01", "eu-de-02"],
        cross_border_transfer_allowed=False
    )
    engine.set_policy(policy)
    
    # Allowed transfer
    req1 = DataTransferRequest(
        tenant_id="tenant-1",
        source_region="eu-de-01",
        destination_region="eu-de-02",
        data_classification="SENSITIVE",
        purpose="backup"
    )
    # Even if destination is allowed, cross_border_transfer_allowed=False means different regions might fail.
    # Actually, in our logic, if source != dest and cross_border=False, it fails.
    assert engine.evaluate_transfer(req1) == "DENIED_CROSS_BORDER_RESTRICTED"
    
    # Allowed transfer (same region)
    req2 = DataTransferRequest(
        tenant_id="tenant-1",
        source_region="eu-de-01",
        destination_region="eu-de-01",
        data_classification="SENSITIVE",
        purpose="processing"
    )
    assert engine.evaluate_transfer(req2) == "ALLOWED"
    
    # Denied (region not allowed)
    req3 = DataTransferRequest(
        tenant_id="tenant-1",
        source_region="eu-de-01",
        destination_region="us-east-1",
        data_classification="SENSITIVE",
        purpose="processing"
    )
    assert engine.evaluate_transfer(req3) == "DENIED_REGION_NOT_ALLOWED"

def test_jurisdiction_aware_routing():
    registry = GlobalServiceRegistry()
    
    registry.register(ServiceEndpoint(service_name="traffic", region_id="eu-de-01", endpoint="https://de.traffic.local"))
    registry.register(ServiceEndpoint(service_name="traffic", region_id="br-01", endpoint="https://br.traffic.local"))
    
    assert registry.route_request("traffic", "eu-de-01") == "https://de.traffic.local"
    assert registry.route_request("traffic", "us-east-1") is None
