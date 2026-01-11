from logging import getLogger
from typing import Any, Sequence

from sqlalchemy import Select
from sqlmodel import SQLModel, func, select

from .exceptions import NotFoundError

logger = getLogger(__name__)


class ReadRepositoryMixin[Model: SQLModel]:

    def base_query(self) -> Select[tuple[Model]]:
        """
        Return the base SELECT query for the model.

        Returns
        -------
        SQLModel.Select
            A SELECT statement targeting the model.
        """
        return select(self.model)

    async def get(self, *, id: int) -> Model | None:
        """
        Retrieve a model instance by primary key.

        Parameters
        ----------
        id
            Primary key of the model.

        Returns
        -------
        Model | None
            The model instance if found, otherwise None.
        """
        return await self.session.get(self.model, id)

    async def get_or_raise(self, *, id: int) -> Model:
        """
        Retrieve a model instance by primary key or raise an error.

        Parameters
        ----------
        id
            Primary key of the model.

        Returns
        -------
        Model
            The retrieved model instance.

        Raises
        ------
        NotFoundError
            If the model instance does not exist.
        """
        obj = await self.get(id=id)

        if not obj:
            raise NotFoundError(f"{self.model.__name__} not found")

        return obj

    async def list(
        self, *, limit: int = 20, offset: int = 0, order_by: Any | None = None
    ) -> Sequence[Model]:
        """
        List model instances with optional pagination and ordering.

        Parameters
        ----------
        limit
            Maximum number of records to return.
        offset
            Number of records to skip.
        order_by
            Optional SQLModel order_by clause.

        Returns
        -------
        Sequence[Model]
            A list of model instances.
        """
        stmt = self.base_query().limit(limit).offset(offset)
        if order_by is not None:
            stmt = stmt.order_by(order_by)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def paginate(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[Sequence[Model], int]:
        """
        Retrieve paginated data along with total record count.

        Parameters
        ----------
        limit
            Maximum number of records to return.
        offset
            Number of records to skip.

        Returns
        -------
        tuple[Sequence[Model], int]
            A tuple containing the data and total record count.
        """
        data_stmt = self.base_query().limit(limit).offset(offset)
        count_stmt = select(func.count()).select_from(self.base_query().subquery())

        data = (await self.session.execute(data_stmt)).scalars().all()
        total = (await self.session.execute(count_stmt)).scalar_one()

        return data, total

    async def exists(self, **filters: Any) -> bool:
        """
        Check whether a record exists matching the given filters.

        Parameters
        ----------
        **filters
            Keyword arguments used as equality filters.

        Returns
        -------
        bool
            True if at least one matching record exists, otherwise False.
        """
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        count = (await self.session.execute(stmt)).scalar_one()
        return count > 0
        return count > 0
