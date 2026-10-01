from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class ConnectorStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    PREPARING = "PREPARING"
    CHARGING = "CHARGING"
    SUSPENDED = "SUSPENDED"
    FINISHING = "FINISHING"
    FAULTED = "FAULTED"
    UNAVAILABLE = "UNAVAILABLE"
    RESERVED = "RESERVED"
    UNKNOWN = "UNKNOWN"

class EVVehicle(BaseModel):
    vehicle_id: str
    tenant_id: str
    vehicle_type: str
    fleet_id: Optional[str] = None
    battery_capacity_kwh: Optional[float] = None
    state_of_charge: Optional[float] = None
    current_location: Optional[dict] = None
    destination: Optional[dict] = None
    charging_state: str = "UNKNOWN"
    energy_consumption_rate: Optional[float] = None
    estimated_range: Optional[float] = None
    timestamp: datetime

class EVConnector(BaseModel):
    connector_id: str
    station_id: str
    connector_type: str
    max_power_kw: float
    current_power_kw: float = 0.0
    voltage: Optional[float] = None
    current: Optional[float] = None
    status: ConnectorStatus = ConnectorStatus.UNKNOWN
    vehicle_id: Optional[str] = None
    session_id: Optional[str] = None

class ChargingStation(BaseModel):
    station_id: str
    tenant_id: str
    site_id: str
    location: dict
    operator: str
    status: str
    connector_count: int
    power_capacity_kw: float
    accessibility: str
    pricing_policy: Optional[str] = None
    grid_connection_id: str
    connectors: List[EVConnector] = []

class EnergyState(BaseModel):
    site_id: str
    grid_import_kw: float
    grid_export_kw: float
    renewable_generation_kw: float
    ev_load_kw: float
    battery_charge_kw: float
    battery_discharge_kw: float
    building_load_kw: float
    available_capacity_kw: float
    timestamp: datetime
    quality: str
