from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class BusinessEntity(Base):
    """B14.1 - Territorial Economic Intelligence Foundation"""
    __tablename__ = "business_entities"
    business_id = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String, index=True) # Retail, Tech, Manufacturing, Logistics
    location = Column(Geometry('POINT'))
    employee_count = Column(Integer)
    status = Column(String)
    established_date = Column(DateTime(timezone=True))

class TourismAsset(Base):
    """B14.5 - Tourism Intelligence"""
    __tablename__ = "tourism_assets"
    asset_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String) # Hotel, Museum, Event, Attraction
    location = Column(Geometry('POINT'))
    capacity = Column(Integer)
    current_occupancy = Column(Integer)
    daily_footfall = Column(Integer)

class EconomicCluster(Base):
    """B14.3 - Economic Cluster Intelligence"""
    __tablename__ = "economic_clusters"
    cluster_id = Column(String, primary_key=True)
    primary_sector = Column(String)
    polygon = Column(Geometry('POLYGON'))
    business_density = Column(Float)
    workforce_size = Column(Integer)
    growth_trend = Column(Float) # +/-% YoY

class InvestmentProject(Base):
    """B14.10 - Investment Intelligence"""
    __tablename__ = "investment_projects"
    project_id = Column(String, primary_key=True)
    sector = Column(String)
    location = Column(Geometry('POINT'))
    capital_required = Column(Float)
    expected_jobs = Column(Integer)
    suitability_score = Column(Float)
    status = Column(String) # PROPOSED, EVALUATING, APPROVED, REJECTED
