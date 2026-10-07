from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class LandParcel(Base):
    """B15.2 - Parcel Intelligence"""
    __tablename__ = "land_parcels"
    parcel_id = Column(String, primary_key=True)
    geometry = Column(Geometry('POLYGON'))
    area_sqm = Column(Float)
    land_use = Column(String) # Residential, Commercial, Industrial, Mixed
    zoning_code = Column(String, index=True)
    development_status = Column(String) # Undeveloped, Developed, Under Construction
    infrastructure_access = Column(Boolean)

class ZoningRule(Base):
    """B15.5 - Zoning Intelligence"""
    __tablename__ = "zoning_rules"
    zone_code = Column(String, primary_key=True)
    permitted_uses = Column(JSON)
    max_height_m = Column(Float)
    max_floor_area_ratio = Column(Float)
    parking_requirements = Column(JSON)

class Building(Base):
    """B15.8 - Building Intelligence"""
    __tablename__ = "buildings"
    building_id = Column(String, primary_key=True)
    parcel_id = Column(String, ForeignKey("land_parcels.parcel_id"))
    geometry = Column(Geometry('POLYGON')) # Footprint
    height_m = Column(Float)
    floors = Column(Integer)
    primary_use = Column(String)
    construction_year = Column(Integer)
    condition_score = Column(Float)

class DevelopmentProposal(Base):
    """B15.12 - Development Proposal Intelligence"""
    __tablename__ = "development_proposals"
    proposal_id = Column(String, primary_key=True)
    parcel_id = Column(String, ForeignKey("land_parcels.parcel_id"))
    proposed_use = Column(String)
    building_area_sqm = Column(Float)
    expected_population = Column(Integer)
    expected_jobs = Column(Integer)
    status = Column(String) # DRAFT, SUBMITTED, REVIEW, APPROVED, REJECTED
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
