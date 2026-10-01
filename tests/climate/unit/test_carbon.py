import pytest
from datetime import datetime, timezone
from src.services.climate.models.schemas import EmissionFactor, DataQuality, ConfidenceLevel
from src.services.climate.engine.carbon import CarbonCalculationEngine

def test_carbon_calculation():
    engine = CarbonCalculationEngine()
    
    factor = EmissionFactor(
        factor_id="EF-1",
        source="EPA",
        publication_date=datetime.now(timezone.utc),
        geographic_scope="US",
        valid_from=datetime.now(timezone.utc),
        unit_activity="kWh",
        unit_emission="kgCO2e",
        factor_value=0.4, # 0.4 kgCO2e per kWh
        methodology="EPA eGRID 2021"
    )
    
    record = engine.calculate_emissions(
        tenant_id="T1",
        source_id="BLDG-1",
        source_category="BUILDINGS",
        activity_type="ELECTRICITY",
        activity_quantity=1000.0, # 1000 kWh
        activity_unit="kWh",
        factor=factor
    )
    
    assert record.emission_quantity == 400.0
    assert record.emission_unit == "kgCO2e"
    assert record.emission_factor_id == "EF-1"

def test_carbon_unit_mismatch():
    engine = CarbonCalculationEngine()
    
    factor = EmissionFactor(
        factor_id="EF-1",
        source="EPA",
        publication_date=datetime.now(timezone.utc),
        geographic_scope="US",
        valid_from=datetime.now(timezone.utc),
        unit_activity="kWh",
        unit_emission="kgCO2e",
        factor_value=0.4, 
        methodology="EPA eGRID 2021"
    )
    
    with pytest.raises(ValueError):
        engine.calculate_emissions(
            tenant_id="T1",
            source_id="VEHICLE-1",
            source_category="TRANSPORT",
            activity_type="DIESEL",
            activity_quantity=100.0, 
            activity_unit="liters", # Mismatch!
            factor=factor
        )
