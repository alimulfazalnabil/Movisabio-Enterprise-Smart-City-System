from src.services.finance.models.schemas import ProjectFinancialModel, EconomicShock
from src.services.finance.engine.project_finance import ProjectFinanceEngine
from src.services.finance.engine.shock_simulation import EconomicShockEngine

def test_project_finance_metrics():
    model = ProjectFinancialModel(
        project_id="PROJ-EV-01",
        capex=500000.0,
        opex=50000.0,
        revenue=120000.0,
        maintenance=10000.0,
        financing_costs=10000.0
    )
    
    engine = ProjectFinanceEngine()
    metrics = engine.calculate_metrics(model)
    
    # Cash Flow = 120000 - 50000 - 10000 - 10000 = 50000
    assert metrics.cash_flow == 50000.0
    # Payback Period = CAPEX / Cash Flow = 500000 / 50000 = 10.0
    assert metrics.payback_period == 10.0

def test_economic_shock_simulation():
    graph = {
        "FUEL_PRICE": ["TRANSPORT", "LOGISTICS", "RETAIL"],
        "FLOOD": ["REAL_ESTATE", "INFRASTRUCTURE"]
    }
    
    engine = EconomicShockEngine(dependency_graph=graph)
    
    shock = EconomicShock(
        shock_id="SHOCK-2026-F1",
        shock_type="FUEL_PRICE",
        magnitude=1.5
    )
    
    impact = engine.simulate_shock(shock)
    assert len(impact.affected_sectors) == 3
    assert "TRANSPORT" in impact.affected_sectors
    # Impact = 3 sectors * 1.5 magnitude * 1000000 = 4500000.0
    assert impact.estimated_economic_impact == 4500000.0
