from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class Campus(Base):
    """B23.23 - Campus Intelligence"""
    __tablename__ = "campuses"
    campus_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String) # UNIVERSITY, HOSPITAL, CORPORATE, GOVERNMENT
    location = Column(Geometry('POLYGON'))
    total_area_sqm = Column(Float)
    current_occupancy = Column(Integer)
    energy_demand_kw = Column(Float)

class Building(Base):
    """B23.2 - Building Digital Twin"""
    __tablename__ = "buildings"
    building_id = Column(String, primary_key=True)
    campus_id = Column(String, ForeignKey("campuses.campus_id"), nullable=True)
    name = Column(String)
    location = Column(Geometry('POLYGON'))
    floor_area_sqm = Column(Float)
    year_built = Column(Integer)
    energy_intensity_kwh_sqm = Column(Float)
    status = Column(String) # OPERATIONAL, MAINTENANCE, EVACUATION

class BuildingAsset(Base):
    """B23.15 - Building Maintenance Intelligence"""
    __tablename__ = "building_assets"
    asset_id = Column(String, primary_key=True)
    building_id = Column(String, ForeignKey("buildings.building_id"))
    type = Column(String) # HVAC, ELEVATOR, PUMP, LIGHTING
    install_date = Column(DateTime(timezone=True))
    condition_score = Column(Float)
    next_maintenance = Column(DateTime(timezone=True))

class BuildingOccupancy(Base):
    """B23.5 - Occupancy Intelligence"""
    __tablename__ = "building_occupancy"
    zone_id = Column(String, primary_key=True)
    building_id = Column(String, ForeignKey("buildings.building_id"))
    max_capacity = Column(Integer)
    current_count = Column(Integer)
    utilization_pct = Column(Float)
    timestamp = Column(DateTime(timezone=True))
