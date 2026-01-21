from typing import Any, Iterable, Sequence

from base.repository import BaseRepository
from sqlmodel import SQLModel, func, select


class ReadRepositoryMixin[Model: SQLModel](BaseRepository[Model]):
    """
    Read-only repository mixin providing common query operations.

    This mixin encapsulates all non-mutating database access patterns,
    including single-entity retrieval, filtered queries, pagination,
    existence checks, and conditional searches.

    It is designed to be composed with other repository mixins to form
    a complete repository implementation.
    """

    async def get(self, *, id: int) -> Model | None:
        """
        Retrieve a single entity by its primary key.

        Parameters
        ----------
        id
            The primary key value of the entity.

        Returns
        -------
        Model | None
            The matching entity if found, otherwise ``None``.
        """
        return await self.session.get(self.model, id)

    async def get_by(self, **filters: Any) -> Model | None:
        """
        Retrieve a single entity matching the given field filters.

        Parameters
        ----------
        **filters
            Keyword arguments mapping model field names to values.

        Returns
        -------
        Model | None
            The matching entity if found, otherwise ``None``.

        Notes
        -----
        If multiple rows match the filters, this method will raise
        an exception from SQLModel.
        """
        stmt = self.base_query().filter_by(**filters)
        return (await self.session.exec(stmt)).one_or_none()

    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Any | None = None,
    ) -> Sequence[Model]:
        """
        Retrieve a paginated list of entities.

        Parameters
        ----------
        limit
            Maximum number of records to return.
        offset
            Number of records to skip before returning results.
        order_by
            Optional SQLAlchemy order expression.

        Returns
        -------
        Sequence[Model]
            A list of retrieved entities.
        """
        stmt = self.base_query(
            limit=limit,
            offset=offset,
            order_by=order_by,
        )

        return (await self.session.exec(stmt)).all()

    async def find_by(
        self,
        *,
        conditions: Iterable[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Any | None = None,
    ) -> Sequence[Model]:
        """
        Retrieve entities matching one or more explicit SQL conditions.

        Parameters
        ----------
        conditions
            An iterable of SQLAlchemy expressions used in WHERE clauses.
        limit
            Maximum number of records to return.
        offset
            Number of records to skip before returning results.
        order_by
            Optional SQLAlchemy order expression.

        Returns
        -------
        Sequence[Model]
            A list of entities matching the provided conditions.
        """
        stmt = self.base_query(
            limit=limit,
            offset=offset,
            order_by=order_by,
        )

        if conditions is not None:
            for condition in conditions:
                stmt = stmt.where(condition)

        return (await self.session.exec(stmt)).all()

    async def exists(self, **filters: Any) -> bool:
        """
        Check whether any entity exists matching the given filters.

        Parameters
        ----------
        **filters
            Keyword arguments mapping model field names to values.

        Returns
        -------
        bool
            ``True`` if at least one matching entity exists, otherwise ``False``.
        """
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        return (await self.session.exec(stmt)).one() > 0
