from typing import Literal

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
