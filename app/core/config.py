from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "dev"  # dev | prod

    app_name: str = "FastAPI Init"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_origins: list[str] = ["127.0.0.1", "localhost"]

    # DBs
    sqlite_db: str = "sqlite+aiosqlite:///./dev.db"
    postgres_db: str | None = None

    @property
    def database_url(self) -> str:
        if self.env == "prod" and self.postgres_db:
            return self.postgres_db
        return self.sqlite_db

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
