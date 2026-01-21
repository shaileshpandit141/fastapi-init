from typing import Any, Sequence

from base.repository import BaseRepository
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel

from ..exceptions import EntityConflictException


class WriteRepositoryMixin[Model: SQLModel, CreateModel: SQLModel | BaseModel](
    BaseRepository[Model]
):
    """
    Mixin providing write (create) operations for SQLModel-based repositories.

    This mixin encapsulates logic for creating single or multiple records
    using an asynchronous SQLModel session. It is designed to be composed
    with other repository mixins and must not be used standalone.

    Type Parameters
    ---------------
    Model
        The SQLModel table type managed by the repository.
    CreateModel
        The schema used to create new instances. This can be either
        a SQLModel or a Pydantic BaseModel.
    """

    async def create(
        self,
        *,
        data: CreateModel,
        values: dict[str, Any] | None = None,
        refresh: bool = True,
    ) -> Model:
        """
        Create and persist a new model instance.

        This method constructs a new database model from the provided
        creation schema, persists it in the database, and optionally
        refreshes the instance after commit.

        Parameters
        ----------
        data
            Schema containing the fields required to create the model.
        values
            Optional additional values injected into the model constructor.
            These values override fields from the creation schema if present.
        refresh
            Whether to refresh the instance after committing the transaction.

        Returns
        -------
        Model
            The newly created and persisted model instance.

        Raises
        ------
        EntityConflictException
            If a database integrity constraint is violated (e.g. unique key).
        """
        try:
            obj = self.model(**data.model_dump(), **(values or {}))
            self.session.add(obj)
            await self.session.commit()

            if refresh:
                await self.session.refresh(obj)

            return obj
        except IntegrityError:
            await self.session.rollback()
            raise EntityConflictException(detail="Resource already exists")

    async def bulk_create(
        self,
        *,
        data: Sequence[CreateModel],
        values: dict[str, Any] | None = None,
        refresh: bool = True,
    ) -> Sequence[Model]:
        """
        Create and persist multiple model instances in a single transaction.

        All instances are created and committed atomically. If any error
        occurs during persistence, the transaction will be rolled back.

        Parameters
        ----------
        data
            A sequence of creation schemas used to construct model instances.
        values
            Optional additional values injected into each model constructor.
        refresh
            Whether to refresh the created instances after committing.

        Returns
        -------
        Sequence[Model]
            A sequence of newly created model instances.
        """
        objs = [self.model(**item.model_dump(), **(values or {})) for item in data]

        self.session.add_all(objs)
        await self.session.commit()

        if refresh:
            await self.session.refresh(objs)

        return objs
