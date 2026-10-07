from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class AgriculturalParcel(Base):
    """B18.2 - Agricultural Land Intelligence"""
    __tablename__ = "agricultural_parcels"
    parcel_id = Column(String, primary_key=True)
    geometry = Column(Geometry('POLYGON'))
    area_hectares = Column(Float)
    soil_type = Column(String)
    irrigation_type = Column(String)
    environmental_constraints = Column(JSON)

class Crop(Base):
    """B18.3 - Crop Intelligence"""
    __tablename__ = "crops"
    crop_id = Column(String, primary_key=True)
    parcel_id = Column(String, ForeignKey("agricultural_parcels.parcel_id"))
    crop_type = Column(String)
    planting_date = Column(DateTime(timezone=True))
    growth_stage = Column(String) # Planted, Vegetative, Flowering, Maturity, Harvested
    expected_yield_tonnes = Column(Float)
    health_status = Column(String)

class Fishery(Base):
    """B18.15 - Fisheries Intelligence"""
    __tablename__ = "fisheries"
    fishery_id = Column(String, primary_key=True)
    fishing_zone = Column(Geometry('POLYGON'))
    target_species = Column(String)
    status = Column(String) # OPEN, CLOSED, RESTRICTED

class FoodSupplyChainNode(Base):
    """B18.20 - Food Supply Chain Intelligence"""
    __tablename__ = "food_supply_nodes"
    node_id = Column(String, primary_key=True)
    node_type = Column(String) # Farm, Warehouse, Processing, Retail
    location = Column(Geometry('POINT'))
    storage_capacity_tonnes = Column(Float)
    current_inventory_tonnes = Column(Float)
    cold_chain_active = Column(Boolean)

class RuralInfrastructure(Base):
    """B18.25 - Rural Infrastructure Intelligence"""
    __tablename__ = "rural_infrastructure"
    infra_id = Column(String, primary_key=True)
    type = Column(String) # Road, Market, Storage, Irrigation
    location = Column(Geometry('GEOMETRY'))
    condition_score = Column(Float)
    accessibility_index = Column(Float)
