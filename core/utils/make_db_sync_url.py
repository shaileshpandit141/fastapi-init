from sqlalchemy.engine.url import make_url


def make_db_sync_url(database_url: str) -> str:

    url = make_url(database_url)

    if url.drivername.startswith("postgresql+"):
        url = url.set(drivername="postgresql")
    elif url.drivername.startswith("sqlite+"):
        url = url.set(drivername="sqlite")

    return str(url)
