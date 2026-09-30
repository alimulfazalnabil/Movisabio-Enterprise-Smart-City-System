from sqlalchemy import Column, String, Float, Integer
from geoalchemy2 import Geometry
from infrastructure.database import Base

class LaneGeometry(Base):
    """
    SQLAlchemy Entity for Lane Management stored in PostGIS.
    """
    __tablename__ = 'lanes'

    lane_id = Column(String, primary_key=True, index=True)
    intersection_id = Column(String, index=True, nullable=False)
    approach = Column(String, nullable=False)  # e.g. "North"
    movement = Column(String, nullable=False)  # e.g. "Left", "Straight", "Right"
    
    # PostGIS geometry types
    polygon = Column(Geometry('POLYGON', srid=4326), nullable=False)
    centerline = Column(Geometry('LINESTRING', srid=4326), nullable=False)
    
    # Operational metadata
    signal_phase = Column(String, nullable=True)
    speed_limit = Column(Float, nullable=False)
    storage_length = Column(Float, nullable=False) # in meters
    saturation_flow = Column(Integer, nullable=False) # vehicles per hour of green
