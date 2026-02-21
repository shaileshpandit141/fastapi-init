from time import sleep

from click import group

from app.adapters.db.session import init_sync_db

from .seeders._command import seed

# =============================================================================
# Check DB Connection.
# =============================================================================


def wait_for_db(retries: int = 5) -> None:
    for _ in range(retries):
        try:
            init_sync_db()
            return
        except Exception:
            sleep(2)

    raise RuntimeError("Database not ready")


# =============================================================================
# Main Cli Entry.
# =============================================================================


@group()
def cli() -> None:
    """A command-line interface to manage FastAPI-Init app."""

    wait_for_db()


# =============================================================================
# Adding All Sub Commands here.
# =============================================================================

cli.add_command(seed)


# =============================================================================
# Run cli app command.
# =============================================================================

if __name__ == "__main__":
    cli()
