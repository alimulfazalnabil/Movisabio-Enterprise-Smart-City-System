"""Application settings loaded from environment variables or a local ``.env``."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AITCSConfiguration(BaseSettings):
    """Runtime endpoints and signal-safety bounds shared by AITCS components."""
    app_name: str = "MoviSabio AITCS Enterprise"
    environment: str = Field(default="production", validation_alias="ENVIRONMENT")
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")
    azure_iot_hub_connection_string: str = Field(default="", validation_alias="AZURE_IOT_HUB_CONNECTION_STRING")
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/movisabio", validation_alias="DATABASE_URL")
    
    # Safety Bounds
    min_green_seconds: int = Field(default=7, description="Absolute minimum green time enforcement")
    max_green_seconds: int = Field(default=120, description="Absolute maximum green time limit")
    yellow_clearance_seconds: int = Field(default=4, description="Standard yellow change interval")
    all_red_clearance_seconds: int = Field(default=2, description="Standard all-red safety interval")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = AITCSConfiguration()
