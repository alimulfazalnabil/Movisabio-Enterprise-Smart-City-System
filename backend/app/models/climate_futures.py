from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class ClimateProjection(Base):
    """B34.1 - Climate Futures Model"""
    __tablename__ = "climate_projections"
    projection_id = Column(String, primary_key=True)
    scenario_pathway = Column(String) # LOW_IMPACT, MODERATE, HIGH_IMPACT
    time_horizon = Column(Integer) # 2030, 2050, 2070
    hazard_type = Column(String) # HEAT, FLOOD, DROUGHT
    spatial_resolution = Column(String)
    expected_value = Column(Float)
    uncertainty_range = Column(JSON) # e.g. {"min": ..., "max": ...}
    confidence_level = Column(String) # HIGH, MEDIUM, LOW

class TerritorialExposure(Base):
    """B34.5 - Climate Exposure Model"""
    __tablename__ = "territorial_exposures"
    exposure_id = Column(String, primary_key=True)
    asset_id = Column(String) # Reference to building/infrastructure
    asset_type = Column(String) # BUILDING, HOSPITAL, GRID
    hazard_type = Column(String)
    projected_vulnerability_score = Column(Float) # Accounts for adaptive capacity
    economic_value_at_risk = Column(Float)

class AdaptationPortfolio(Base):
    """B34.9 - Climate-Adaptation Portfolio"""
    __tablename__ = "adaptation_portfolios"
    portfolio_id = Column(String, primary_key=True)
    territory_id = Column(String)
    interventions = Column(JSON) # List of proposed adaptation strategies
    estimated_cost = Column(Float)
    projected_risk_reduction_pct = Column(Float)
    nature_based_solutions_included = Column(Boolean, default=False)
