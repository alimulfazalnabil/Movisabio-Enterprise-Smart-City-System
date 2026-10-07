from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class InfrastructureAsset(Base):
    """B11.1 - Universal Infrastructure Asset Model"""
    __tablename__ = "infrastructure_assets"
    asset_id = Column(String, primary_key=True)
    asset_class = Column(String, index=True) # Transportation, Water, Energy, Buildings, Telecom
    asset_type = Column(String) # Road, Pump, Transformer
    location = Column(Geometry('GEOMETRY'))
    installation_date = Column(DateTime(timezone=True))
    expected_life_years = Column(Float)
    criticality = Column(String) # CRITICAL, HIGH, MEDIUM, LOW
    lifecycle_stage = Column(String) # PLANNED, INSTALLED, OPERATING, DEGRADED
    data_quality = Column(String)

class AssetCondition(Base):
    """B11.5 - Asset Condition Intelligence"""
    __tablename__ = "asset_conditions"
    condition_id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("infrastructure_assets.asset_id"), index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    state = Column(String) # EXCELLENT, GOOD, FAIR, DEGRADED, POOR, CRITICAL, UNKNOWN
    score = Column(Float) # 0 to 100
    estimated_rul_months = Column(Float) # B11.8 - Remaining Useful Life
    confidence = Column(Float)

class AssetRisk(Base):
    """B11.12 - Infrastructure Risk Model"""
    __tablename__ = "asset_risks"
    risk_id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("infrastructure_assets.asset_id"), index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    failure_probability = Column(Float)
    consequence_score = Column(Float)
    risk_level = Column(String) # LOW, MEDIUM, HIGH, CRITICAL

class AssetDependency(Base):
    """B11.10 - Asset Dependency Graph"""
    __tablename__ = "asset_dependencies"
    dependency_id = Column(String, primary_key=True)
    source_asset_id = Column(String, ForeignKey("infrastructure_assets.asset_id"), index=True)
    target_asset_id = Column(String, ForeignKey("infrastructure_assets.asset_id"), index=True)
    dependency_type = Column(String) # POWER, WATER, ACCESS

class AssetWorkOrder(Base):
    """B11.22 - Infrastructure Work Orders"""
    __tablename__ = "asset_work_orders"
    work_order_id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("infrastructure_assets.asset_id"), index=True)
    priority = Column(String)
    problem_description = Column(String)
    status = Column(String) # OPEN, ASSIGNED, IN_PROGRESS, VERIFIED, CLOSED
    deadline = Column(DateTime(timezone=True))
