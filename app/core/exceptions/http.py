from ._base import AppError

# =============================================================================
# Http level error.
# =============================================================================


class HttpError(AppError):
    """Base http errors."""

    status_code: int

    def __init_subclass__(cls, status_code: int) -> None:
        cls.status_code = status_code
        return super().__init_subclass__()


# =============================================================================
# Unauthorized error.
# =============================================================================


class UnauthorizedError(HttpError, status_code=401):
    """Base unauthorized errors."""

    pass


# =============================================================================
# Access denied error.
# =============================================================================


class AccessDeniedError(HttpError, status_code=403):
    """Base access denied errors."""

    pass


# =============================================================================
# Conflict error.
# =============================================================================


class ConflictError(HttpError, status_code=409):
    """Base conflict errors."""

    pass
