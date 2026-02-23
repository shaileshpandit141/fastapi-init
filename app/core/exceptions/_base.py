# =============================================================================
# Base application error.
# =============================================================================


class AppError(Exception):
    """Base class for all application errors."""

    def __init__(self, deatil: object) -> None:
        self.detail = deatil
