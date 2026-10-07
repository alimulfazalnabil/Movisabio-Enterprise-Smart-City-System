from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class CanonicalTerritory(Base):
    """B50.7 - Canonical Entity Hierarchy (Root Node)"""
    __tablename__ = "core_territories"
    territory_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String) # CITY, REGION, NATION, SUPRANATIONAL
    boundary_geojson = Column(JSON)
    sovereignty_level = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class CanonicalOrganization(Base):
    """B50.7 - Canonical Entity Hierarchy"""
    __tablename__ = "core_organizations"
    org_id = Column(String, primary_key=True)
    name = Column(String)
    org_type = Column(String) # GOVERNMENT, ENTERPRISE, RESEARCH
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    headquarters_territory = Column(String, ForeignKey("core_territories.territory_id"))

class CanonicalAsset(Base):
    """B50.7 - Canonical Entity Hierarchy"""
    __tablename__ = "core_assets"
    asset_id = Column(String, primary_key=True)
    name = Column(String)
    asset_type = Column(String) # CAMERA, SIGNAL, SENSOR, BUILDING, FLEET
    territory_id = Column(String, ForeignKey("core_territories.territory_id"))
    owner_org_id = Column(String, ForeignKey("core_organizations.org_id"))
    location_geometry = Column(JSON)
    status = Column(String)

class PlatformDeploymentEnvironment(Base):
    """B50.22 - Environment Strategy"""
    __tablename__ = "core_environments"
    env_id = Column(String, primary_key=True)
    name = Column(String) # DEV, STAGING, PILOT, PRODUCTION
    deployment_model = Column(String) # SAAS, SOVEREIGN, EDGE, PRIVATE_CLOUD
    region = Column(String)
    status = Column(String)
