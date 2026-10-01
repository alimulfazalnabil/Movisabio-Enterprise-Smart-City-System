import pytest
from src.services.infrastructure.models.schemas import AssetDependency
from src.services.infrastructure.engine.dependency import DependencyGraphEngine

def test_dependency_engine_single_impact():
    dependencies = [
        AssetDependency(
            source_asset_id="SUBSTATION-1",
            target_asset_id="TRAFFIC_SIGNAL-1",
            dependency_type="POWERED_BY",
            criticality="HIGH",
            direction="FORWARD",
            confidence=1.0
        )
    ]
    
    engine = DependencyGraphEngine(dependencies)
    impacted = engine.get_downstream_impact("SUBSTATION-1")
    
    assert impacted == ["TRAFFIC_SIGNAL-1"]

def test_dependency_engine_cascade_impact():
    dependencies = [
        AssetDependency(
            source_asset_id="GRID-1",
            target_asset_id="SUBSTATION-1",
            dependency_type="SUPPLIES",
            criticality="HIGH",
            direction="FORWARD",
            confidence=1.0
        ),
        AssetDependency(
            source_asset_id="SUBSTATION-1",
            target_asset_id="EV_CHARGER-1",
            dependency_type="POWERED_BY",
            criticality="MEDIUM",
            direction="FORWARD",
            confidence=1.0
        )
    ]
    
    engine = DependencyGraphEngine(dependencies)
    impacted = engine.get_downstream_impact("GRID-1")
    
    assert "SUBSTATION-1" in impacted
    assert "EV_CHARGER-1" in impacted
    assert len(impacted) == 2

def test_dependency_engine_circular_dependency():
    dependencies = [
        AssetDependency(
            source_asset_id="PUMP-1",
            target_asset_id="GENERATOR-1",
            dependency_type="COOLS",
            criticality="HIGH",
            direction="FORWARD",
            confidence=1.0
        ),
        AssetDependency(
            source_asset_id="GENERATOR-1",
            target_asset_id="PUMP-1",
            dependency_type="POWERS",
            criticality="HIGH",
            direction="FORWARD",
            confidence=1.0
        )
    ]
    
    engine = DependencyGraphEngine(dependencies)
    impacted = engine.get_downstream_impact("PUMP-1")
    
    # Should resolve gracefully without infinite loop
    assert "GENERATOR-1" in impacted
    assert "PUMP-1" in impacted
    assert len(impacted) == 2
