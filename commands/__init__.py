from time import sleep

from click import group

from core.db.init_db import init_db

from .create import create
from .seed import seed


def wait_for_db(retries: int = 5) -> None:
    for _ in range(retries):
        try:
            init_db()
            return
        except Exception:
            sleep(2)

    raise RuntimeError("Database not ready")


@group()
def cli() -> None:
    """A command-line interface to manage FastAPI-Init app."""
    wait_for_db()


cli.add_command(create)
cli.add_command(seed)
