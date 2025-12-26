from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: Literal["dev", "prod"] = "dev"  # dev | prod

    # App Config
    app_name: str = "FastAPI Init"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_origins: list[str] = ["127.0.0.1", "localhost"]
    async_db_url: str = "sqlite+aiosqlite:///../db.sqlite3"

    # Model Config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
