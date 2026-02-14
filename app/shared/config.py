from typing import Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

# =============================================================================
# Core application settings.
# =============================================================================


class AppSettings(BaseSettings):
    """
    Core application settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    APP_NAME: str = "MyApp"
    APP_ENV: Literal["local", "development", "staging", "production"] = "local"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True


# =============================================================================
# Database configuration.
# =============================================================================


class DatabaseSettings(BaseSettings):
    """
    Database configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    NAME: str = "app"

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            path=self.NAME,
        )


# =============================================================================
# Redis configuration.
# =============================================================================


class RedisSettings(BaseSettings):
    """
    Redis configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    HOST: str = "localhost"
    PORT: int = 6379
    DB: int = 0

    @property
    def dsn(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.HOST,
            port=self.PORT,
            path=str(self.DB),
        )


# =============================================================================
# JWT configuration.
# =============================================================================


class JWTSettings(BaseSettings):
    """
    JWT configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    SECRET_KEY: str = "super-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 7


# =============================================================================
# Celery / async messaging configuration.
# =============================================================================


class CelerySettings(BaseSettings):
    """
    Celery / async messaging configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="CELERY_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    BROKER_URL: str = "redis://localhost:6379/1"
    RESULT_BACKEND: str = "redis://localhost:6379/2"
