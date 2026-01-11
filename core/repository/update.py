from logging import getLogger
from typing import Any

from sqlmodel import SQLModel, select

logger = getLogger(__name__)


class UpdateRepositoryMixin[Model: SQLModel, UpdateModel: SQLModel]:

    async def update(self, *, obj: Model, data: UpdateModel) -> Model:
        """
        Update a model instance using an update schema.

        Only fields explicitly set on the update model are applied.

        Parameters
        ----------
        obj
            The existing model instance.
        data
            SQLModel containing update data.

        Returns
        -------
        Model
            The updated and refreshed model instance.
        """
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(obj, field, value)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def patch(self, *, id: int, data: dict[str, Any]) -> Model:
        """
        Partially update a model instance using a raw dictionary.

        Parameters
        ----------
        id
            Primary key of the model.
        data
            Dictionary of fields and values to update.

        Returns
        -------
        Model
            The updated model instance.

        Raises
        ------
        NotFoundError
            If the model instance does not exist.
        """
        obj = await self.get_or_raise(id=id)
        for field, value in data.items():
            setattr(obj, field, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def upsert(self, *, lookup: dict[str, Any], data: dict[str, Any]) -> Model:
        """
        Update an existing record or create a new one if it does not exist.

        Parameters
        ----------
        lookup
            Fields used to locate an existing record.
        data
            Fields to update or set on creation.

        Returns
        -------
        Model
            The upserted model instance.
        """
        stmt = select(self.model).filter_by(**lookup)
        obj = (await self.session.execute(stmt)).scalar_one_or_none()

        if obj:
            for k, v in data.items():
                setattr(obj, k, v)
        else:
            obj = self.model(**lookup, **data)
            self.session.add(obj)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj
