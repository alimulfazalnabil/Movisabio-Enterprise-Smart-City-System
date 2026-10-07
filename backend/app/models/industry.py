from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class Factory(Base):
    """B22.3 - Factory Digital Twin"""
    __tablename__ = "factories"
    factory_id = Column(String, primary_key=True)
    name = Column(String)
    industry_sector = Column(String)
    location = Column(Geometry('POLYGON'))
    production_capacity = Column(Float)
    current_utilization_pct = Column(Float)
    energy_intensity = Column(Float)
    status = Column(String) # OPERATIONAL, DEGRADED, MAINTENANCE, OFFLINE

class Machine(Base):
    """B22.8 - Predictive Maintenance"""
    __tablename__ = "machines"
    machine_id = Column(String, primary_key=True)
    factory_id = Column(String, ForeignKey("factories.factory_id"))
    type = Column(String)
    operating_hours = Column(Integer)
    health_score = Column(Float)
    last_maintenance = Column(DateTime(timezone=True))
    estimated_rul_days = Column(Integer) # Remaining Useful Life

class Supplier(Base):
    """B22.13 - Raw Material Intelligence"""
    __tablename__ = "suppliers"
    supplier_id = Column(String, primary_key=True)
    name = Column(String)
    material_provided = Column(String)
    geographic_region = Column(String)
    reliability_score = Column(Float)
    average_lead_time_days = Column(Integer)

class Shipment(Base):
    """B22.22 - Freight Digital Twin"""
    __tablename__ = "shipments"
    shipment_id = Column(String, primary_key=True)
    origin_id = Column(String)
    destination_id = Column(String)
    transport_mode = Column(String) # ROAD, RAIL, SEA, AIR
    current_location = Column(Geometry('POINT'))
    status = Column(String) # PLANNED, IN_TRANSIT, DELAYED, DELIVERED
    eta = Column(DateTime(timezone=True))
