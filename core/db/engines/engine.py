from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from core.settings import settings
from core.utils.make_db_sync_url import make_db_sync_url

engine: Engine = create_engine(
    url=make_db_sync_url(settings.database_url),
    echo=settings.env == "dev",
)
