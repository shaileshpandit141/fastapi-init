from typing import Any, Iterable, Sequence, cast

from base.repository import BaseRepository
from sqlalchemy.orm import Load, selectinload
from sqlmodel import SQLModel


def build_selectinload(model: type[SQLModel], relation_path: str) -> Load:
    """
    Build a nested selectinload option from a dot-separated relationship path.

    Example
    -------
    build_selectinload(Author, "books.publisher.address")

    Produces
    --------
    selectinload(Author.books)
        .selectinload(Book.publisher)
        .selectinload(Publisher.address)
    """
    parts = relation_path.split(".")

    attr = getattr(model, parts[0])
    loader = selectinload(attr)

    current = attr.property.mapper.class_

    for part in parts[1:]:
        attr = getattr(current, part)
        loader = loader.selectinload(attr)
        current = attr.property.mapper.class_

    return cast(Load, loader)


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

        for path in relations:
            stmt = stmt.options(build_selectinload(self.model, path))

        result = await self.session.exec(stmt)
        return result.all()
