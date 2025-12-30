from datetime import datetime, timedelta, timezone


def get_utc_now(add: timedelta | None = None) -> datetime:
    """Get the current UTC datetime, optionally adding a timedelta."""

    if add:
        return datetime.now(timezone.utc) + add

    return datetime.now(timezone.utc)
