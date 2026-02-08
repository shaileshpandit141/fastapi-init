from typing import Any, Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel

from ..base.repository import BaseRepository


class UpdateRepositoryMixin[Model: SQLModel, UpdateModel: SQLModel | BaseModel](
    BaseRepository[Model]
):
    """
    Mixin providing update operations for SQLModel-based repositories.

    This mixin encapsulates logic for updating existing model instances
    using either structured update schemas or raw dictionaries. It is
    intended to be composed with other repository mixins and must not
    be used standalone.

    Type Parameters
    ---------------
    Model
        The SQLModel table type managed by the repository.
    UpdateModel
        The schema used to update an existing model. This can be either
        a SQLModel or a Pydantic BaseModel.
    """

    async def update(self, *, obj: Model, data: UpdateModel) -> Model:
        """
        Update a model instance using an update schema.

        Only fields explicitly set on the update schema are applied
        to the model instance. Unset fields are ignored.

        Parameters
        ----------
        obj
            The existing model instance to update.
        data
            Schema containing the fields to update.

        Returns
        -------
        Model
            The updated and refreshed model instance.

        Notes
        -----
        - This method commits the transaction immediately.
        - The instance is refreshed after commit to ensure
          database-generated values are loaded.
        """
        updates = data.model_dump(exclude_unset=True)

        for k, v in updates.items():
            setattr(obj, k, v)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def bulk_update(
        self,
        *,
        objs: list[Model],
        data: list[UpdateModel],
    ) -> list[Model]:
        """
        Bulk update multiple model instances using update schemas.

        Each update schema is applied to the corresponding model instance
        by position.

        Parameters
        ----------
        objs
            List of existing model instances to update.
        data
            List of update schemas.

        Returns
        -------
        list[Model]
            The updated and refreshed model instances.

        Raises
        ------
        ValueError
            If the lengths of objs and data do not match.
        """
        if len(objs) != len(data):
            raise ValueError("objs and data must have the same length")

        for obj, update in zip(objs, data, strict=True):
            updates = update.model_dump(exclude_unset=True)
            for k, v in updates.items():
                setattr(obj, k, v)
            self.session.add(obj)

        await self.session.commit()

        for obj in objs:
            await self.session.refresh(obj)

        return objs

    async def patch(self, *, obj: Model, data: dict[str, Any]) -> Model:
        """
        Partially update a model instance using a raw dictionary.

        This method applies all key-value pairs from the provided
        dictionary directly to the model instance without schema
        validation.

        Parameters
        ----------
        obj
            The existing model instance to update.
        data
            Dictionary of fields and values to apply to the model.

        Returns
        -------
        Model
            The updated and refreshed model instance.

        Notes
        -----
        - This method commits the transaction immediately.
        - Use with caution, as no validation is performed on input data.
        """
        for k, v in data.items():
            setattr(obj, k, v)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def bulk_patch(
        self,
        *,
        objs: list[Model],
        data: list[dict[str, Any]],
    ) -> list[Model]:
        """
        Bulk partially update multiple model instances using raw dictionaries.

        Parameters
        ----------
        objs
            List of existing model instances to update.
        data
            List of dictionaries containing fields and values to apply.

        Returns
        -------
        list[Model]
            The updated and refreshed model instances.

        Raises
        ------
        ValueError
            If the lengths of objs and data do not match.
        """
        if len(objs) != len(data):
            raise ValueError("objs and data must have the same length")

        for obj, patch in zip(objs, data, strict=True):
            for k, v in patch.items():
                setattr(obj, k, v)
            self.session.add(obj)

        await self.session.commit()

        for obj in objs:
            await self.session.refresh(obj)

        return objs

    async def bulk_set(
        self,
        *,
        objs: Sequence[Model],
        data: dict[str, Any],
    ) -> Sequence[Model]:
        """
        Bulk update multiple model instances with the same field values.

        This is useful for flag-style updates such as marking records
        as read, archived, deleted, etc.

        Parameters
        ----------
        objs
            List of existing model instances to update.
        data
            Dictionary of fields and values to apply to all instances.

        Returns
        -------
        list[Model]
            The updated and refreshed model instances.
        """
        for obj in objs:
            for k, v in data.items():
                setattr(obj, k, v)
            self.session.add(obj)

        await self.session.commit()

        for obj in objs:
            await self.session.refresh(obj)

        return objs
