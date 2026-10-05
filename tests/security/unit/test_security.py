from src.services.security.models.schemas import Threat, CyberPhysicalAsset, ResilienceScenario
from src.services.security.engine.risk import RiskEngine
from src.services.security.engine.resilience import ResilienceEngine

def test_risk_calculation():
    threat = Threat(
        threat_id="CVE-2026-9999",
        type="RCE",
        severity="CRITICAL", # 4
        exploitability="HIGH" # 3
    )
    
    asset = CyberPhysicalAsset(
        asset_id="TRAFFIC-CTRL-01",
        asset_type="TRAFFIC_CONTROLLER",
        criticality="CRITICAL", # 4
        exposure="INTERNET" # 2
    )
    
    engine = RiskEngine()
    # 4 + 3 + 4 + 2 = 13 -> CRITICAL
    risk_score = engine.calculate_risk(threat, asset)
    assert risk_score == "CRITICAL"

def test_resilience_simulation():
    # Dependency graph: Cloud -> Edge -> Controller
    graph = {
        "CLOUD_API": ["EDGE_GATEWAY"],
        "EDGE_GATEWAY": ["TRAFFIC_CONTROLLER_1", "TRAFFIC_CONTROLLER_2"]
    }
    
    engine = ResilienceEngine(dependency_graph=graph)
    
    scenario = ResilienceScenario(
        scenario_id="SCENARIO-01",
        target_asset_id="EDGE_GATEWAY",
        failure_type="NETWORK_ISOLATION"
    )
    
    impacted_assets = engine.simulate_scenario(scenario)
    assert "EDGE_GATEWAY" in impacted_assets
    assert "TRAFFIC_CONTROLLER_1" in impacted_assets
    assert "TRAFFIC_CONTROLLER_2" in impacted_assets
    assert "CLOUD_API" not in impacted_assets
