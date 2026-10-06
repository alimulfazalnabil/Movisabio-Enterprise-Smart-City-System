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

class OperatingModeEnum(str, enum.Enum):
    OFF = "OFF"
    MANUAL = "MANUAL"
    SIMULATION = "SIMULATION"
    HIL = "HIL"
    SHADOW = "SHADOW"
    ASSISTED = "ASSISTED"
    LIMITED_AUTOMATIC = "LIMITED_AUTOMATIC"
    AUTHORIZED_AUTOMATIC = "AUTHORIZED_AUTOMATIC"
    EMERGENCY = "EMERGENCY"
    FAILSAFE = "FAILSAFE"

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
    mode = Column(Enum(OperatingModeEnum))

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

class Incident(Base):
    __tablename__ = "incidents"
    incident_id = Column(String, primary_key=True)
    intersection_id = Column(String, ForeignKey("intersections.intersection_id"))
    severity = Column(String)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    detected_by = Column(String)
    description = Column(String)
    root_cause = Column(String)
    resolution = Column(String)
    status = Column(String)

class HumanOverride(Base):
    __tablename__ = "human_overrides"
    override_id = Column(Integer, primary_key=True, autoincrement=True)
    intersection_id = Column(String, ForeignKey("intersections.intersection_id"))
    operator_id = Column(String)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ai_recommendation = Column(JSON)
    operator_decision = Column(String)
    reason = Column(String)
    result = Column(String)

class PilotDataset(Base):
    __tablename__ = "pilot_datasets"
    dataset_id = Column(String, primary_key=True)
    site_id = Column(String)
    time_range_start = Column(DateTime(timezone=True))
    time_range_end = Column(DateTime(timezone=True))
    source = Column(String)
    model_version = Column(String)
    privacy_classification = Column(String)

class Corridor(Base):
    __tablename__ = "corridors"
    corridor_id = Column(String, primary_key=True)
    tenant_id = Column(String)
    city_id = Column(String)
    name = Column(String)
    geometry = Column(Geometry('LINESTRING'))
    direction = Column(String)
    speed_profile = Column(JSON)
    capacity_profile = Column(JSON)
    operating_policy = Column(String)
    status = Column(String)

class CorridorIntersection(Base):
    __tablename__ = "corridor_intersections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    corridor_id = Column(String, ForeignKey("corridors.corridor_id"))
    intersection_id = Column(String, ForeignKey("intersections.intersection_id"))
    sequence_order = Column(Integer)

class IntersectionRelationship(Base):
    __tablename__ = "intersection_relationships"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String, ForeignKey("intersections.intersection_id"))
    target_id = Column(String, ForeignKey("intersections.intersection_id"))
    relationship_type = Column(String) # UPSTREAM, DOWNSTREAM, PARALLEL, FEEDER
    distance_m = Column(Float)
    travel_time_s = Column(Float)

class CorridorState(Base):
    __tablename__ = "corridor_states"
    state_id = Column(Integer, primary_key=True, autoincrement=True)
    corridor_id = Column(String, ForeignKey("corridors.corridor_id"), index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    vehicle_count = Column(Integer)
    flow = Column(Float)
    average_speed = Column(Float)
    density = Column(Float)
    occupancy = Column(Float)
    queue_length = Column(Float)
    travel_time = Column(Float)
    delay = Column(Float)
    stops = Column(Float)
    spillback_risk = Column(Float)
    bottleneck_score = Column(Float)
    congestion_level = Column(Enum(TrafficStateEnum))
    incident_state = Column(String)
    data_quality = Column(String)
