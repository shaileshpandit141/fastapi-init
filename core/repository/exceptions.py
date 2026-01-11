from core.exceptions import AppError


class RepositoryError(AppError):
    pass


class NotFoundError(RepositoryError):
    pass


class ConflictError(RepositoryError):
    pass
