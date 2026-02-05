from typing import Any, Iterable

from sqlmodel import SQLModel, delete, select

from ..base.repository import BaseRepository
from ..exceptions import EntityNotFoundError


class DeleteRepositoryMixin[Model: SQLModel](BaseRepository[Model]):
    """
    Delete repository mixin providing entity deletion operations.

    This mixin supports:
    - Deleting a single persisted entity instance
    - Deleting an entity by arbitrary filters
    - Bulk deletion by primary keys
    - Bulk deletion using SQLAlchemy expressions

    Designed to be composed with other repository mixins.
    """

    async def delete(self, *, obj: Model) -> None:
        """
        Delete a single entity instance.

        Parameters
        ----------
        obj
            Persisted model instance to be deleted.

        Notes
        -----
        This method commits the transaction immediately.
        """
        await self.session.delete(obj)
        await self.session.commit()

    async def delete_by(self, **filters: Any) -> None:
        """
        Delete a single entity matching the given filters.

        Parameters
        ----------
        **filters
            Keyword arguments used to filter the entity.

        Raises
        ------
        EntityNotFoundError
            If no matching entity exists.
        """
        stmt = select(self.model).filter_by(**filters)
        obj = (await self.session.exec(stmt)).one_or_none()

        if not obj:
            raise EntityNotFoundError(detail="Resource does not exist")

        await self.delete(obj=obj)

    async def bulk_delete(self, *, ids: Iterable[int]) -> int:
        """
        Delete multiple entities by their primary key values.

        Parameters
        ----------
        ids
            Iterable of entity primary key values.

        Returns
        -------
        int
            Number of rows deleted.
        """
        stmt = delete(self.model).where(
            self.model.id.in_(ids)  # type: ignore[attr-defined]
        )

        result = await self.session.exec(stmt)
        await self.session.commit()

        return result.rowcount or 0

    async def bulk_delete_by(self, *, conditions: Iterable[Any]) -> int:
        """
        Delete multiple entities using custom SQLAlchemy conditions.

        Parameters
        ----------
        conditions
            Iterable of SQLAlchemy WHERE clause expressions.

        Returns
        -------
        int
            Number of rows deleted.
        """
        stmt = delete(self.model)

        for condition in conditions:
            stmt = stmt.where(condition)

        result = await self.session.exec(stmt)
        await self.session.commit()

        return result.rowcount or 0
