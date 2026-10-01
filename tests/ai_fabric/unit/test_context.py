import pytest
from src.services.ai_fabric.engine.context import TerritorialContextEngine

def test_context_engine():
    engine = TerritorialContextEngine()
    
    context = engine.build_context("TERR-1", "INT-001")
    
    assert context["territory_id"] == "TERR-1"
    assert context["target_id"] == "INT-001"
    assert context["traffic_state"] == "CONGESTED"
    assert context["flood_risk"] == "ELEVATED"
    assert "context_version" in context
