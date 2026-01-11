from sqlmodel import SQLModel

from .base import AsyncBaseRepository
from .create import CreateRepositoryMixin
from .delete import DeleteRepositoryMixin
from .locking import LockingRepositoryMixin
from .read import ReadRepositoryMixin
from .update import UpdateRepositoryMixin


class AsyncSQLRepository[Model: SQLModel, CreateModel: SQLModel, UpdateModel: SQLModel](
    AsyncBaseRepository[Model],
    CreateRepositoryMixin[Model, CreateModel],
    ReadRepositoryMixin[Model],
    UpdateRepositoryMixin[Model, UpdateModel],
    DeleteRepositoryMixin[Model],
    LockingRepositoryMixin[Model],
):
    pass
