from ._base import AppError

# =============================================================================
# Domain level error.
# =============================================================================


class DomainError(AppError):
    """Base domain errors."""

    pass


# =============================================================================
# Already exists error.
# =============================================================================


class AlreadyExistsError(DomainError):
    """Base already exists errors."""

    pass


# =============================================================================
# NotFound error.
# =============================================================================


class NotFoundError(DomainError):
    """Base not found errors."""

    pass
