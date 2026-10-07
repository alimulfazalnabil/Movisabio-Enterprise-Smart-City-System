from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class UtilityAsset(Base):
    """B16.1 - Unified Territorial Resource Model"""
    __tablename__ = "utility_assets"
    asset_id = Column(String, primary_key=True)
    utility_type = Column(String, index=True) # Energy, Water, Fuel
    asset_type = Column(String) # Substation, Transformer, Pump, Pipeline
    location = Column(Geometry('GEOMETRY'))
    capacity = Column(Float)
    current_load = Column(Float)
    health_score = Column(Float)
    status = Column(String)

class GenerationAsset(Base):
    """B16.2 - Energy Intelligence Foundation"""
    __tablename__ = "generation_assets"
    generation_id = Column(String, primary_key=True)
    type = Column(String) # Solar, Wind, Hydro
    location = Column(Geometry('POINT'))
    max_capacity_mw = Column(Float)
    current_output_mw = Column(Float)
    status = Column(String)

class StorageAsset(Base):
    """B16.6 - Battery & Energy Storage Intelligence"""
    __tablename__ = "storage_assets"
    storage_id = Column(String, primary_key=True)
    type = Column(String) # Battery, PumpedHydro
    capacity_mwh = Column(Float)
    state_of_charge = Column(Float) # 0.0 to 1.0
    charge_status = Column(String) # CHARGING, DISCHARGING, IDLE

class EVChargingStation(Base):
    """B16.10 - EV Charging Intelligence"""
    __tablename__ = "ev_charging_stations"
    station_id = Column(String, primary_key=True)
    location = Column(Geometry('POINT'))
    total_ports = Column(Integer)
    available_ports = Column(Integer)
    current_power_draw_kw = Column(Float)
    grid_capacity_limit_kw = Column(Float)

class UtilityOutage(Base):
    """B16.18 - Utility Outage Intelligence"""
    __tablename__ = "utility_outages"
    outage_id = Column(String, primary_key=True)
    utility_type = Column(String)
    affected_area = Column(Geometry('POLYGON'))
    start_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    customers_affected = Column(Integer)
    severity = Column(String)
    status = Column(String) # DETECTED, CONFIRMED, RESPONSE, RECOVERY, RESTORED
