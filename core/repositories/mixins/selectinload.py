from typing import Any, Iterable, Sequence, cast

from base.repository import BaseRepository
from sqlalchemy.orm import Load, selectinload
from sqlmodel import SQLModel


def build_selectinload(model: type[SQLModel], relation_path: str) -> Load:
    """
    Build a nested `selectinload` option from a dot-separated relationship path.

    This utility enables eager-loading of arbitrarily deep relationship graphs
    using SQLAlchemy's `selectinload` strategy.

    Parameters
    ----------
    model : type[SQLModel]
        The root SQLModel class from which the relationship path starts.
    relation_path : str
        Dot-separated relationship path.

        Example:
            "books.publisher.address"

    Returns
    -------
    Load
        A SQLAlchemy `Load` option suitable for use with `stmt.options(...)`.

    Example
    -------
    build_selectinload(Author, "books.publisher.address")

    Produces
    --------
    selectinload(Author.books)
        .selectinload(Book.publisher)
        .selectinload(Publisher.address)

    Notes
    -----
    - All path components must be valid SQLAlchemy relationship attributes.
    - This function assumes relationship traversal only (no column paths).
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


class SelectionloadRepositoryMixin[Model: SQLModel](BaseRepository[Model]):
    """
    Repository mixin providing `selectinload`-based eager loading support.

    This mixin enables retrieval of entities along with nested related data
    using SQLAlchemy's `selectinload` strategy. It is designed for predictable,
    N+1-safe loading in async environments.

    Intended to be composed with other repository mixins.

    Features
    --------
    - Eager loading via `selectinload`
    - Support for nested relationship paths (dot-separated)
    - Filtering via keyword arguments or SQLAlchemy conditions
    - Pagination via `limit` and `offset`
    - Strong compatibility with async SQLModel usage

    Design Notes
    ------------
    - This mixin **only** performs `selectinload`
    - Other loading strategies (joinedload, subqueryload) should be exposed
      via separate mixins or methods for clarity
    """

    async def get_selectinload(
        self, *, relations: Iterable[str], **filters: Any
    ) -> Model | None:
        """
        Fetch a single entity with related data eagerly loaded via `selectinload`.

        Parameters
        ----------
        relations : Iterable[str]
            Dot-separated relationship paths to eager load.

            Example:
                ["books", "books.publisher"]
        **filters : Any
            Field-value pairs applied using `filter_by`.

        Returns
        -------
        Model | None
            The first entity matching the filters, with requested relationships
            eagerly loaded, or None if no match is found.

        Notes
        -----
        - Intended for lookups that are expected to return at most one row
        - For complex filtering, prefer `list_selectinload` with conditions
        """
        stmt = self.base_query()

        if filters:
            stmt = stmt.filter_by(**filters)

        if relations:
            for rel in relations:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.exec(stmt)
        return result.first()

    async def list_selectinload(
        self,
        *,
        relations: Iterable[str],
        conditions: Iterable[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Any = None,
    ) -> Sequence[Model]:
        """
        Fetch multiple entities with related data eagerly loaded via `selectinload`.

        Parameters
        ----------
        relations : Iterable[str]
            Dot-separated relationship paths to eager load.

            Example:
                ["books", "books.publisher.address"]
        conditions : Iterable[Any] | None
            SQLAlchemy boolean expressions used with `WHERE`.

            Example:
                [Author.is_active == True]
        limit : int | None
            Maximum number of rows to return.
        offset : int | None
            Number of rows to skip.
        order_by : Any
            SQLAlchemy `order_by` expression.

            Example:
                Author.name.asc()

        Returns
        -------
        Sequence[Model]
            List of entities matching the query, with requested relationships loaded.

        Performance Notes
        -----------------
        - Uses `selectinload`, resulting in:
            1 query for base entities
            N additional queries for relationships
        - Suitable for one-to-many and many-to-many relationships
        """
        stmt = self.base_query(limit=limit, offset=offset, order_by=order_by)

        if conditions:
            for condition in conditions:
                stmt = stmt.where(condition)

        for path in relations:
            stmt = stmt.options(build_selectinload(self.model, path))

        result = await self.session.exec(stmt)
        return result.all()
