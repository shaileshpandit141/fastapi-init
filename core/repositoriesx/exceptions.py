from core.exceptions import AppError


class UnitOfWorkError(AppError):
    """Raised when a UnitOfWork transaction fails."""

    pass


class RepositoryError(AppError):
    """Base exception for repository-related errors."""

    pass


class EntityNotFoundError(RepositoryError):
    """
    Raised when a requested entity cannot be found
    in the database.
    """

    pass


class EntityConflictError(RepositoryError):
    """
    Raised when attempting to create or update
    an entity that violates a uniqueness constraint.
    """

    pass
