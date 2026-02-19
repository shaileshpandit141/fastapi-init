from datetime import datetime, timezone

# =============================================================================
# Function That Return Current Time with UTC Format.
# =============================================================================


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)
