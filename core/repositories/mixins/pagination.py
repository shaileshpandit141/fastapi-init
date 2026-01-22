from typing import Any, Sequence

from sqlmodel import SQLModel, func, select

from ..base.repository import BaseRepository


class PaginationMixin[Model: SQLModel](BaseRepository[Model]):
    """
    Pagination repository mixin providing offset-based pagination support.

    This mixin exposes a single method for retrieving a paginated subset
    of records along with the total record count, which is commonly
    required for API responses and UI pagination controls.

    It is intended to be composed with other repository mixins.
    """

    async def paginate(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Any = None,
    ) -> tuple[Sequence[Model], int]:
        """
        Retrieve a paginated list of entities along with the total count.

        Parameters
        ----------
        limit
            Maximum number of records to return.
        offset
            Number of records to skip before returning results.

        Returns
        -------
        tuple[Sequence[Model], int]
            A tuple containing:
            - A sequence of retrieved entities.
            - The total number of records available (ignoring pagination).
        """
        stmt = self.base_query(
            limit=limit,
            offset=offset,
            order_by=order_by,
        )
        count_stmt = select(func.count()).select_from(self.base_query().subquery())

        data = (await self.session.exec(stmt)).all()
        total = (await self.session.exec(count_stmt)).one()

        return data, total
