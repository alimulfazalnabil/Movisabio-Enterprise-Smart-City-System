from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator
from functools import lru_cache
from typing import List, Optional
import os

class Settings(BaseSettings):
    """
    Enterprise Configuration Management.
    """
    # Application
    APP_NAME: str = "MoviSabio"
    APP_ENV: str = "development" # development, testing, staging, production
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database & Cache
    DATABASE_URL: str
    REDIS_URL: str

    # Authentication
    FRONTEND_CORS_ORIGINS: str = "*"
    API_RATE_LIMIT: int = 100
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "RS256"
    JWT_ISSUER: str = "movisabio-identity"
    JWT_AUDIENCE: str = "movisabio-api"

    # API
    CORS_ORIGINS: List[str] = ["*"]
    
    # Observability
    LOG_LEVEL: str = "INFO"
    OTEL_ENABLED: bool = False
    OTEL_ENDPOINT: Optional[str] = None

    # Messaging
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883

    # Traffic Control Safety Engine
    TRAFFIC_CONTROLLER_MODE: str = "simulation" # simulation, live
    TRAFFIC_CONTROLLER_TIMEOUT: float = 2.0
    TRAFFIC_CONTROLLER_RETRY_LIMIT: int = 3
    SAFETY_VALIDATION: bool = True
    REQUIRE_CONTROLLER_ACKNOWLEDGEMENT: bool = True
    ALLOW_REMOTE_CONTROL: bool = False
    EMERGENCY_OVERRIDE_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('APP_ENV', 'development')}",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @model_validator(mode='after')
    def validate_production_safety(self) -> 'Settings':
        # Security: Production must not have DEBUG enabled
        if self.APP_ENV == "production" and self.DEBUG:
            raise ValueError("DEBUG mode cannot be enabled in production environment.")
            
        # Security: CORS cannot be '*' in production
        if self.APP_ENV == "production" and "*" in self.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS must be strictly defined in production (cannot be '*').")
            
        # Safety: Traffic Control strict validation
        if self.APP_ENV == "production" and self.TRAFFIC_CONTROLLER_MODE == "live":
            if not self.SAFETY_VALIDATION:
                raise ValueError("CRITICAL SAFETY ERROR: SAFETY_VALIDATION cannot be disabled when TRAFFIC_CONTROLLER_MODE is 'live' in production.")
                
        return self

@lru_cache()
def get_settings(env_override: Optional[str] = None) -> Settings:
    """
    Returns the cached configuration object.
    Loads standard .env as fallback if specific environment file does not exist.
    """
    env = env_override or os.getenv('APP_ENV', 'development')
    env_file = f".env.{env}"
    if not os.path.exists(env_file):
        env_file = ".env"
    
    return Settings(_env_file=env_file)
