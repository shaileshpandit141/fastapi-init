from time import sleep

from click import group

from app.adapters.db.session import init_sync_db

from .seed.group import seed_group
from .user.group import user_group

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
def cli_group() -> None:
    """Entry point for the FastAPI-Init command-line interface."""

    wait_for_db()


# =============================================================================
# Adding All Sub groups here.
# =============================================================================

cli_group.add_command(seed_group)
cli_group.add_command(user_group)

# =============================================================================
# Run cli group.
# =============================================================================

if __name__ == "__main__":
    cli_group()
