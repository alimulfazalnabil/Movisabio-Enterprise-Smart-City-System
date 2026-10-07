from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class CriticalSystem(Base):
    """B33.2 - Critical Systems Registry"""
    __tablename__ = "critical_systems"
    system_id = Column(String, primary_key=True)
    name = Column(String)
    domain = Column(String) # ENERGY, WATER, HEALTHCARE, TELECOM
    territory_id = Column(String)
    criticality_level = Column(String) # TIER_1, TIER_2, TIER_3
    dependencies = Column(JSON) # List of system_ids this depends on

class EssentialService(Base):
    """B33.6 - Essential Services Model"""
    __tablename__ = "essential_services"
    service_id = Column(String, primary_key=True)
    system_id = Column(String, ForeignKey("critical_systems.system_id"))
    name = Column(String)
    minimum_viable_service_level_pct = Column(Float)
    current_service_level_pct = Column(Float)
    recovery_time_objective_hours = Column(Integer)

class EmergencyResourceReserve(Base):
    """B33.13 - Strategic Reserve Intelligence"""
    __tablename__ = "emergency_resource_reserves"
    reserve_id = Column(String, primary_key=True)
    resource_type = Column(String) # FUEL, WATER, MEDICINE
    location_id = Column(String)
    current_quantity = Column(Float)
    daily_consumption_rate = Column(Float)
    days_of_coverage_est = Column(Float)
