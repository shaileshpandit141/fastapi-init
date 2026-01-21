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
    """
    Full-featured asynchronous repository composed from mixins.

    This repository combines CRUD, read, pagination, and deletion
    operations into a single reusable class.

    It is designed to manage a single SQLModel entity type and
    its corresponding creation and update schemas.

    Type Parameters
    ---------------
    Model
        The SQLModel table type managed by this repository.
    CreateModel
        Schema used for creating new entities (SQLModel or Pydantic BaseModel).
    UpdateModel
        Schema used for updating existing entities (SQLModel or Pydantic BaseModel).

    Notes
    -----
    - All database operations are async and assume an active AsyncSession
      provided to the underlying BaseRepository.
    - This class does not implement domain-specific logic; it is intended
      to be used as a base repository in service layers or for composition.
    """

    pass
