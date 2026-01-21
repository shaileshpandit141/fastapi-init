from core.exceptions import AppException


class RepositoryException(AppException):
    """Base exception for repository-related errors."""

    pass


class EntityNotFoundException(RepositoryException):
    """
    Raised when a requested entity cannot be found
    in the database.
    """

    pass


class EntityConflictException(RepositoryException):
    """
    Raised when attempting to create or update
    an entity that violates a uniqueness constraint.
    """

    pass
