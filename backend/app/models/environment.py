from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class EnvironmentalSensor(Base):
    """B10.1 - Environmental Data Fabric"""
    __tablename__ = "environmental_sensors"
    sensor_id = Column(String, primary_key=True)
    sensor_type = Column(String) # AirQuality, Weather, Noise, Water
    location = Column(Geometry('POINT'))
    status = Column(String)
    health = Column(String)
    calibration_version = Column(String)

class EnvironmentalObservation(Base):
    """B10.1 - Universal Environmental Observation"""
    __tablename__ = "environmental_observations"
    observation_id = Column(String, primary_key=True)
    source_id = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    location = Column(Geometry('POINT'))
    parameter = Column(String) # PM2.5, Temperature, WaterLevel, dB
    value = Column(Float)
    unit = Column(String)
    quality = Column(String) # VALID, SUSPECT, STALE, INVALID, MISSING, UNKNOWN (B10.3)
    confidence = Column(Float)
    data_provenance = Column(String)

class AirQualityState(Base):
    """B10.5 - Air Quality Intelligence"""
    __tablename__ = "air_quality_states"
    state_id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(Geometry('POINT'))
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    pollutants = Column(JSON) # e.g. {"PM2.5": 68, "NO2": 45}
    aqi = Column(Float)
    dominant_pollutant = Column(String)
    trend = Column(String)
    confidence = Column(Float)
    data_quality = Column(String)

class EnvironmentalEvent(Base):
    """B10.10 - Environmental Event Detection"""
    __tablename__ = "environmental_events"
    event_id = Column(String, primary_key=True)
    event_type = Column(String) # AIR_QUALITY_DETERIORATION, FLOOD_RISK, HEAT_EVENT
    location = Column(Geometry('POLYGON'))
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    severity = Column(String)
    status = Column(String) # DETECTED, VALIDATED, ASSESSED, RESPONDED, CLOSED
    correlation_data = Column(JSON) # e.g., correlated mobility/traffic events

class CarbonInventory(Base):
    """B10.21 - Carbon Intelligence"""
    __tablename__ = "carbon_inventories"
    inventory_id = Column(String, primary_key=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    scope_1 = Column(Float)
    scope_2 = Column(Float)
    scope_3 = Column(Float)
    methodology = Column(String)
    boundary = Column(String)
    data_source = Column(String)
    uncertainty = Column(Float)

class ClimateHazard(Base):
    """B10.23 - Climate Risk Intelligence"""
    __tablename__ = "climate_hazards"
    hazard_id = Column(String, primary_key=True)
    hazard_type = Column(String) # Flood, Heat, Storm
    exposure_zone = Column(Geometry('POLYGON'))
    vulnerability_score = Column(Float)
    risk_level = Column(String)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
