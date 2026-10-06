from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone
import enum

class TrafficStateEnum(str, enum.Enum):
    FREE = "FREE"
    LIGHT = "LIGHT"
    MODERATE = "MODERATE"
    HEAVY = "HEAVY"
    SEVERE = "SEVERE"
    UNKNOWN = "UNKNOWN"

class SignalModeEnum(str, enum.Enum):
    SIMULATION = "SIMULATION"
    SHADOW = "SHADOW"
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"
    FAULT = "FAULT"

class Camera(Base):
    __tablename__ = "cameras"
    camera_id = Column(String, primary_key=True)
    site_id = Column(String, index=True)
    stream_url = Column(String)
    protocol = Column(String)
    resolution = Column(String)
    fps = Column(Integer)
    location = Column(Geometry('POINT'))
    orientation = Column(String)
    calibration = Column(JSON)
    status = Column(String)
    configuration_version = Column(String)

class Intersection(Base):
    __tablename__ = "intersections"
    intersection_id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(Geometry('POINT'))

class Lane(Base):
    __tablename__ = "lanes"
    lane_id = Column(String, primary_key=True)
    intersection_id = Column(String, ForeignKey("intersections.intersection_id"))
    direction = Column(String)
    movement = Column(String)
    speed_limit = Column(Float)
    geometry = Column(Geometry('POLYGON'))
    
class TrafficState(Base):
    __tablename__ = "traffic_states"
    state_id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String, ForeignKey("intersections.intersection_id"), index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    vehicle_count = Column(Integer)
    flow = Column(Float)
    average_speed = Column(Float)
    occupancy = Column(Float)
    queue_length = Column(Float)
    density = Column(Float)
    congestion_level = Column(Enum(TrafficStateEnum))
    data_quality = Column(String, default="VALID")
    lane_states = Column(JSON)

class TrafficSignal(Base):
    __tablename__ = "traffic_signals"
    signal_id = Column(String, primary_key=True)
    intersection_id = Column(String, ForeignKey("intersections.intersection_id"))
    controller_id = Column(String)
    phase = Column(String)
    phase_start = Column(DateTime(timezone=True))
    elapsed = Column(Float)
    remaining = Column(Float)
    health = Column(String)
    mode = Column(Enum(SignalModeEnum))

class SignalCommand(Base):
    __tablename__ = "signal_commands"
    command_id = Column(String, primary_key=True)
    intersection_id = Column(String, ForeignKey("intersections.intersection_id"))
    signal_id = Column(String, ForeignKey("traffic_signals.signal_id"))
    requested_phase = Column(String)
    duration = Column(Float)
    source = Column(String)
    model_version = Column(String)
    policy_version = Column(String)
    safety_result = Column(String)
    authorization = Column(String)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String)
