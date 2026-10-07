from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class CellSite(Base):
    """B24.6 - Mobile Network Intelligence"""
    __tablename__ = "cell_sites"
    site_id = Column(String, primary_key=True)
    operator = Column(String)
    technologies = Column(JSON) # e.g. ["4G", "5G"]
    location = Column(Geometry('POINT'))
    coverage_radius_m = Column(Float)
    current_utilization_pct = Column(Float)
    status = Column(String) # ACTIVE, DEGRADED, OFFLINE

class FiberRoute(Base):
    """B24.4 - Fiber Network Intelligence"""
    __tablename__ = "fiber_routes"
    route_id = Column(String, primary_key=True)
    name = Column(String)
    geometry = Column(Geometry('LINESTRING'))
    capacity_gbps = Column(Float)
    utilization_gbps = Column(Float)
    redundancy_level = Column(String) # HIGH, MEDIUM, NONE

class DataCenter(Base):
    """B24.16 - Data Center Intelligence"""
    __tablename__ = "data_centers"
    dc_id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(Geometry('POLYGON'))
    it_load_kw = Column(Float)
    total_facility_load_kw = Column(Float)
    current_pue = Column(Float)

class IoTDevice(Base):
    """B24.11 - IoT Device Lifecycle"""
    __tablename__ = "iot_devices"
    device_id = Column(String, primary_key=True)
    type = Column(String) # TRAFFIC_CAM, AIR_QUALITY, WATER_METER
    location = Column(Geometry('POINT'))
    status = Column(String) # ACTIVE, STALE, OFFLINE
    battery_level_pct = Column(Float, nullable=True)
    last_seen = Column(DateTime(timezone=True))
