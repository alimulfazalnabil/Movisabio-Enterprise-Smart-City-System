from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Centralized Configuration & Secrets Management.
    Inherited by all MoviSabio platform modules.
    """
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Platform APIs
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "MoviSabio Territorial Intelligence Platform"
    
    # Security / Identity
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database
    DATABASE_URL: str
    
    # Regional Data Policy (EU vs LatAm)
    ENFORCE_DATA_RESIDENCY: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings():
    return Settings()
