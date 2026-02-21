from time import sleep

from click import group

from app.adapters.db.session import init_sync_db

from .seed._command import seed_command
from .user.group import user_command_group

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
def main_command() -> None:
    """A command-line interface to manage FastAPI-Init app."""

    wait_for_db()


# =============================================================================
# Adding All Sub Commands here.
# =============================================================================

main_command.add_command(seed_command, name="seed")
main_command.add_command(user_command_group, name="user")

# =============================================================================
# Run cli app command.
# =============================================================================

if __name__ == "__main__":
    main_command()
