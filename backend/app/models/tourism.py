from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class TourismAsset(Base):
    """B21.2 - Tourism Asset Intelligence"""
    __tablename__ = "tourism_assets"
    asset_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String) # Natural, Museum, Entertainment
    location = Column(Geometry('POINT'))
    max_daily_capacity = Column(Integer)
    environmental_sensitivity = Column(String) # LOW, MEDIUM, HIGH
    current_visitor_count = Column(Integer)

class HeritageSite(Base):
    """B21.11 - Cultural Heritage Intelligence"""
    __tablename__ = "heritage_sites"
    site_id = Column(String, primary_key=True)
    name = Column(String)
    historical_period = Column(String)
    location = Column(Geometry('POLYGON'))
    conservation_status = Column(String) # INTACT, DEGRADING, AT_RISK, UNDER_REPAIR
    vulnerability_factors = Column(JSON) # e.g. ["Humidity", "Vibration"]

class TourismEvent(Base):
    """B21.15 - Event Intelligence"""
    __tablename__ = "tourism_events"
    event_id = Column(String, primary_key=True)
    name = Column(String)
    venue_location = Column(Geometry('POLYGON'))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    expected_attendance = Column(Integer)
    infrastructure_impact_level = Column(String) # LOW, MODERATE, HIGH, SEVERE

class DestinationCapacity(Base):
    """B21.5 - Destination Capacity Intelligence"""
    __tablename__ = "destination_capacity"
    zone_id = Column(String, primary_key=True)
    hotel_occupancy_pct = Column(Float)
    parking_utilization_pct = Column(Float)
    water_stress_index = Column(Float)
    waste_capacity_pct = Column(Float)
    overall_pressure_status = Column(String) # NORMAL, ELEVATED, OVERTOURISM
