from core.exceptions import AppException


class RepositoryException(AppException):
    """Base repository exception"""

    pass


class EntityNotFoundException(RepositoryException):
    """Entity not found in storage"""

    pass


class EntityConflictException(RepositoryException):
    """Unique constraint violation"""

    pass
