import pytest
from datetime import datetime, timezone, timedelta
from src.services.energy.engine.charging import SmartChargingEngine

def test_charging_power_calculation_normal():
    engine = SmartChargingEngine()
    
    # 50 kWh battery, 20% to 80% (needs 30 kWh) in 2 hours
    # requires 15 kW constant
    allocated = engine.calculate_charging_power(
        vehicle_soc=20.0,
        target_soc=80.0,
        battery_capacity_kwh=50.0,
        departure_time=datetime.now(timezone.utc) + timedelta(hours=2),
        available_capacity_kw=100.0,
        max_charger_power_kw=50.0
    )
    
    assert allocated == pytest.approx(15.0, 0.1)

def test_charging_power_capped_by_charger():
    engine = SmartChargingEngine()
    
    # Needs 30 kWh in 1 hour (requires 30 kW)
    # But charger max is 22 kW
    allocated = engine.calculate_charging_power(
        vehicle_soc=20.0,
        target_soc=80.0,
        battery_capacity_kwh=50.0,
        departure_time=datetime.now(timezone.utc) + timedelta(hours=1),
        available_capacity_kw=100.0,
        max_charger_power_kw=22.0
    )
    
    assert allocated == 22.0

def test_charging_power_capped_by_grid():
    engine = SmartChargingEngine()
    
    # Needs 30 kWh in 1 hour (requires 30 kW)
    # Charger max is 50 kW, but grid only has 10 kW left
    allocated = engine.calculate_charging_power(
        vehicle_soc=20.0,
        target_soc=80.0,
        battery_capacity_kwh=50.0,
        departure_time=datetime.now(timezone.utc) + timedelta(hours=1),
        available_capacity_kw=10.0,
        max_charger_power_kw=50.0
    )
    
    assert allocated == 10.0

def test_charging_stops_when_target_reached():
    engine = SmartChargingEngine()
    
    allocated = engine.calculate_charging_power(
        vehicle_soc=80.0,
        target_soc=80.0,
        battery_capacity_kwh=50.0,
        departure_time=datetime.now(timezone.utc) + timedelta(hours=1),
        available_capacity_kw=100.0,
        max_charger_power_kw=50.0
    )
    
    assert allocated == 0.0
