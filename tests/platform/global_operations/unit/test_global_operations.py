from src.platform.global_operations.sovereignty.zone import SovereigntyEngine, SovereigntyZone
from src.platform.global_operations.federation.service_catalog import GlobalServiceCatalog, GlobalServiceStatus
from src.platform.global_operations.incident_federation.major_incident import GlobalIncidentEngine, MajorIncident, GlobalIncidentStatus

def test_sovereignty_engine():
    engine = SovereigntyEngine()
    zone_br = SovereigntyZone(
        zone_id="zone-br",
        geography="Brazil",
        data_residency_required=True,
        operational_authority="BR-Ops"
    )
    zone_eu = SovereigntyZone(
        zone_id="zone-eu",
        geography="Europe",
        data_residency_required=True,
        operational_authority="EU-Ops"
    )
    engine.register_zone(zone_br)
    engine.register_zone(zone_eu)
    
    # Should not allow transfer out of zone if residency is required
    can_transfer = engine.check_data_transfer("zone-br", "zone-eu")
    assert can_transfer is False
    
    # Within zone is fine
    can_transfer = engine.check_data_transfer("zone-br", "zone-br")
    assert can_transfer is True

def test_global_service_catalog():
    catalog = GlobalServiceCatalog()
    s1 = GlobalServiceStatus(
        service_id="traffic-opt",
        region_id="br-south-1",
        tenant_id="t-1",
        version="v1.0",
        health_status="HEALTHY"
    )
    s2 = GlobalServiceStatus(
        service_id="traffic-opt",
        region_id="eu-west-1",
        tenant_id="t-2",
        version="v1.1",
        health_status="DEGRADED"
    )
    catalog.register_regional_service(s1)
    catalog.register_regional_service(s2)
    
    health = catalog.query_global_health("traffic-opt")
    assert health["br-south-1"] == "HEALTHY"
    assert health["eu-west-1"] == "DEGRADED"

def test_global_incident_engine():
    engine = GlobalIncidentEngine()
    incident = MajorIncident(
        global_incident_id="g-inc-1",
        title="Global Identity Outage",
        impacted_regions=["eu-west-1"]
    )
    engine.declare_major_incident(incident)
    engine.add_impacted_region("g-inc-1", "br-south-1", "reg-inc-44")
    
    inc = engine.major_incidents["g-inc-1"]
    assert "br-south-1" in inc.impacted_regions
    assert "reg-inc-44" in inc.regional_incident_refs
