from logging import getLogger
from typing import Any, Sequence

from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel

from .exceptions import ConflictError

logger = getLogger(__name__)


class CreateRepositoryMixin[Model: SQLModel, CreateModel: SQLModel]:

    async def create(
        self,
        *,
        data: CreateModel,
        refresh: bool = True,
        include: set[str] | None = None,
        exclude: set[str] | None = None,
        extra_fields: dict[str, Any] | None = None,
    ) -> Model:
        """
        Create and persist a new model instance.

        Parameters
        ----------
        data
            SQLModel containing the creation data.
        refresh
            Whether to refresh the instance after commit.
        include
            Fields to include when dumping the create model.
        exclude
            Fields to exclude when dumping the create model.
        extra_fields
            Additional fields to inject into the model constructor.

        Returns
        -------
        Model
            The newly created model instance.

        Raises
        ------
        ConflictError
            If a database integrity constraint is violated.
        """
        try:
            obj = self.model(
                **data.model_dump(include=include, exclude=exclude),
                **(extra_fields or {}),
            )

            self.session.add(obj)
            await self.session.commit()

            if refresh:
                await self.session.refresh(obj)

            return obj
        except IntegrityError as error:
            logger.debug(
                f"{self.__class__.__name__} record creation failed: ",
                exc_info=error,
            )
            await self.session.rollback()
            raise ConflictError from error

    async def bulk_create(
        self,
        *,
        data: Sequence[CreateModel],
        refresh: bool = True,
        include: set[str] | None = None,
        exclude: set[str] | None = None,
        extra_fields: dict[str, Any] | None = None,
    ) -> Sequence[Model]:
        """
        Create multiple model instances in a single transaction.

        Parameters
        ----------
        data
            A sequence of SQLModel creation objects.
        refresh
            Whether to refresh the created instances after commit.
        include
            Fields to include when dumping the create models.
        exclude
            Fields to exclude when dumping the create models.
        extra_fields
            Additional fields to inject into each model constructor.

        Returns
        -------
        Sequence[Model]
            The created model instances.
        """
        objs = [
            self.model(
                **item.model_dump(include=include, exclude=exclude),
                **(extra_fields or {}),
            )
            for item in data
        ]

        self.session.add_all(objs)
        await self.session.commit()

        if refresh:
            await self.session.refresh(objs)

        return objs
