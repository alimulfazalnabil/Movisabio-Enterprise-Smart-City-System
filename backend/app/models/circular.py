from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class SmartBin(Base):
    """B17.5 - Smart Bin Intelligence"""
    __tablename__ = "smart_bins"
    bin_id = Column(String, primary_key=True)
    location = Column(Geometry('POINT'))
    waste_type = Column(String) # Organic, Plastic, Paper, Mixed
    capacity_kg = Column(Float)
    current_fill_level_pct = Column(Float)
    sensor_health = Column(String) # VALID, SUSPECT, STALE
    last_collection = Column(DateTime(timezone=True))

class WasteFacility(Base):
    """B17.8 - Waste Facility Intelligence"""
    __tablename__ = "waste_facilities"
    facility_id = Column(String, primary_key=True)
    type = Column(String) # Transfer, Recycling, Composting, Landfill
    location = Column(Geometry('POLYGON'))
    processing_capacity_tpd = Column(Float)
    current_load_tpd = Column(Float)
    status = Column(String)

class MaterialOffer(Base):
    """B17.14 - Circular Material Marketplace"""
    __tablename__ = "material_offers"
    offer_id = Column(String, primary_key=True)
    provider_id = Column(String)
    material_type = Column(String)
    quantity_kg = Column(Float)
    purity_pct = Column(Float)
    price_per_kg = Column(Float)
    status = Column(String) # AVAILABLE, RESERVED, SOLD

class CollectionRoute(Base):
    """B17.7 - Real-Time Waste Routing"""
    __tablename__ = "collection_routes"
    route_id = Column(String, primary_key=True)
    vehicle_id = Column(String)
    waste_type = Column(String)
    stops = Column(JSON) # List of bin_ids
    estimated_duration_min = Column(Integer)
    status = Column(String) # PLANNED, ACTIVE, COMPLETED
