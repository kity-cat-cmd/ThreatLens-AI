"""
Configuration management for ThreatLens AI
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # AI Configuration
    ai_provider: str = "openai"
    ai_api_key: Optional[str] = None
    ai_model: str = "gpt-4"

    # Database Configuration
    database_url: str = "sqlite:///./threatlens.db"

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    redis_enabled: bool = False

    # Cache Configuration
    cache_ttl: int = 3600

    # Logging
    log_level: str = "INFO"

    # Security
    secret_key: str = "change-this-in-production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
