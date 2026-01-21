from pydantic import BaseModel
from sqlmodel import SQLModel

from .mixins.delete import DeleteRepositoryMixin
from .mixins.pagination import PaginationMixin
from .mixins.read import ReadRepositoryMixin
from .mixins.update import UpdateRepositoryMixin
from .mixins.write import WriteRepositoryMixin


class Repository[
    Model: SQLModel,
    CreateModel: SQLModel | BaseModel,
    UpdateModel: SQLModel | BaseModel,
](
    DeleteRepositoryMixin[Model],
    PaginationMixin[Model],
    ReadRepositoryMixin[Model],
    UpdateRepositoryMixin[Model, UpdateModel],
    WriteRepositoryMixin[Model, CreateModel],
):
    """Async repository composed from mixins."""

    pass
