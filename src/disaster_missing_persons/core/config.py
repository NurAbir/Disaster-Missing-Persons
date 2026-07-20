"""Application configuration management."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Disaster Missing Persons"
    DEBUG: bool = False

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "disaster_missing_persons"

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Image processing
    MAX_IMAGE_SIZE_MB: int = 5
    IMAGE_QUALITY: int = 60
    THUMBNAIL_WIDTH: int = 300
    THUMBNAIL_HEIGHT: int = 300

    # Report settings
    REPORT_AUTO_EXPIRE_DAYS: int = 30

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Default admin
    DEFAULT_ADMIN_EMAIL: str = "admin@disaster-response.org"
    DEFAULT_ADMIN_PASSWORD: str = "admin123"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
