from functools import lru_cache
from typing import Literal

from cryptography.fernet import Fernet
from pydantic import EmailStr, Field
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
    NAME: str = "FastAPI-Init"
    ENV: Literal["local", "development", "staging", "production"] = "local"
    API_VERSION_PREFIX: str = "/api/v1"
    DEBUG: bool = True


# =============================================================================
# CORS configuration.
# =============================================================================


class CORSSettings(BaseSettings):
    """
    CORS configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="CORS_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    ALLOW_ORIGINS: list[str] = ["127.0.0.1", "localhost"]
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True


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
    def async_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )

    @property
    def sync_dsn(self) -> str:
        return (
            f"postgresql+psycopg://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )


# =============================================================================
# Email configuration.
# =============================================================================


class EmailSettings(BaseSettings):
    """
    Email / SMTP configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="EMAIL_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Provider mode
    PROVIDER: Literal["smtp", "console", "disabled"] = "console"

    # SMTP configuration
    HOST: str = "localhost"
    PORT: int = 1025
    USERNAME: str | None = None
    PASSWORD: str | None = None

    USE_TLS: bool = True
    USE_SSL: bool = False

    # Sender defaults
    FROM_EMAIL: EmailStr = "noreply@example.com"
    FROM_NAME: str = "MyApp"

    # Timeout (seconds)
    TIMEOUT: int = Field(default=10, ge=1)

    @property
    def is_enabled(self) -> bool:
        return self.PROVIDER != "disabled"

    @property
    def is_smtp(self) -> bool:
        return self.PROVIDER == "smtp"


# =============================================================================
# JWT configuration.
# =============================================================================


class EncryptionSettings(BaseSettings):
    """
    Encryption configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="Encryption_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    KEY: str = Fernet.generate_key().decode()


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
    PASSWORD: str | None = None

    SSL: bool = False

    SOCKET_TIMEOUT: int = 5
    SOCKET_CONNECT_TIMEOUT: int = 5

    MAX_CONNECTIONS: int = 10

    @property
    def url(self) -> str:
        scheme = "rediss" if self.SSL else "redis"
        auth = f":{self.PASSWORD}@" if self.PASSWORD else ""
        return f"{scheme}://{auth}{self.HOST}:{self.PORT}/{self.DB}"


# =============================================================================
# Celery configuration.
# =============================================================================


class CelerySettings(BaseSettings):
    """
    Celery configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="CELERY_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    BROKER_URL: str = "redis://localhost:6379/1"
    RESULT_BACKEND: str = "redis://localhost:6379/2"

    TASK_SERIALIZER: str = "json"
    RESULT_SERIALIZER: str = "json"
    ACCEPT_CONTENT: list[str] = ["json"]

    TIMEZONE: str = "UTC"
    ENABLE_UTC: bool = True


# =============================================================================
# Central configuration container.
# =============================================================================


class Settings:
    """
    Central configuration container.
    """

    def __init__(self) -> None:
        self.app = AppSettings()
        self.cors = CORSSettings()
        self.db = DatabaseSettings()
        self.redis = RedisSettings()
        self.encryption = EncryptionSettings()
        self.jwt = JWTSettings()
        self.celery = CelerySettings()
        self.email = EmailSettings()


# =============================================================================
# Cached settings instance.
# =============================================================================


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    """
    return Settings()
