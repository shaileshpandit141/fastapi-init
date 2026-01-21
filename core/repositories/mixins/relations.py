from typing import Any, Iterable, Sequence

from base.repository import BaseRepository
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel


class RelationsRepositoryMixin[Model: SQLModel](BaseRepository[Model]):
    """
    Mixin to fetch related entities with optional filtering, eager loading, and pagination.

    This mixin can be combined with other repository mixins to provide flexible
    data retrieval that includes related entities and supports arbitrary filters.

    Features
    --------
    - Filtering by keyword arguments or SQLAlchemy conditions
    - Eager loading of relationships via `selectinload`
    - Optional pagination using `limit` and `offset`
    - Optional ordering using `order_by`
    """

    async def get_with_relations(
        self, *, relations: Iterable[str], **filters: Any
    ) -> Model | None:
        """
        Fetch a single entity matching the provided filters, including related entities.

        Parameters
        ----------
        relations : Iterable[str]
            Names of relationship attributes to eager load.
        **filters : Any
            Arbitrary field-value pairs to filter the entity.

        Returns
        -------
        Model | None
            The first entity matching the filters with requested relationships loaded,
            or None if no entity is found.
        """
        stmt = self.base_query()

        if filters:
            stmt = stmt.filter_by(**filters)

        if relations:
            for rel in relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.exec(stmt)
        return result.first()

    async def list_with_relations(
        self,
        *,
        relations: Iterable[str],
        conditions: Iterable[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Any = None,
    ) -> Sequence[Model]:
        """
        List entities matching conditions, including related entities, with optional pagination and ordering.

        Parameters
        ----------
        relations : Iterable[str]
            Names of relationship attributes to eager load.
        conditions : Iterable[Any] | None
            SQLAlchemy expressions to filter the query (e.g., `[Model.field == value]`).
        limit : int | None
            Maximum number of entities to return. If None, returns all matching entities.
        offset : int | None
            Number of entities to skip before returning results.
        order_by : Any
            SQLAlchemy order_by expression to sort the results.

        Returns
        -------
        Sequence[Model]
            List of entities matching the conditions with requested relationships loaded.
        """
        stmt = self.base_query(limit=limit, offset=offset, order_by=order_by)

        if conditions:
            for condition in conditions:
                stmt = stmt.where(condition)

        if relations:
            for rel in relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.exec(stmt)
        return result.all()
