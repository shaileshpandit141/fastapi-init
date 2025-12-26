from datetime import datetime, timezone


def get_current_utc() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)
