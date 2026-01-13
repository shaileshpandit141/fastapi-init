import secrets
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: Literal["dev", "prod"] = "dev"  # dev | prod

    # App Config
    app_name: str = "FastAPI Init"
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    # Security & Auth Config
    allow_origins: list[str] = ["127.0.0.1", "localhost"]
    database_url: str = "sqlite+aiosqlite:///./db.sqlite"
    redis_url: str = "redis://localhost:6379/0"
    access_token_secret_key: str = secrets.token_hex(32)
    refresh_token_secret_key: str = secrets.token_hex(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_minutes: int = 30

    # Logging Config
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Email and Celery Config
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: str = ""
    email_password: str = ""
    email_from: str = ""
    celery_broker_url: str = "redis://localhost:6379/0"

    # Model Config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Singleton instance
settings = Settings()
