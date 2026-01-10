# pyright: reportCallIssue=false

from logging import getLogger
from typing import Any, Iterable, Sequence, cast

from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, delete, func, select

from .exceptions import ConflictError, NotFoundError

logger = getLogger(__name__)


class AsyncSessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class AsyncCRUDService[Model: SQLModel, CreateModel: SQLModel, UpdateModel: SQLModel]:
    """
    Generic asynchronous CRUD service for SQLModel entities.

    This service provides common create, read, update, delete, and utility
    operations for a given SQLModel model using an AsyncSession.

    Type Parameters
    ---------------
    Model
        A SQLModel table class.
    CreateModel
        A SQLModel used for object creation.
    UpdateModel
        A SQLModel used for object updates.

    Notes
    -----
    - All write operations commit the session.
    - Errors related to missing or conflicting records are translated into
      domain-specific exceptions.
    """

    def __init__(self, *, session: AsyncSession, model: type[Model]) -> None:
        """
        Initialize the CRUD service.

        Parameters
        ----------
        session
            An active SQLModel AsyncSession.
        model
            The SQLModel managed by this service.
        """
        self.session = session
        self.model = model

    def base_query(self) -> Select[tuple[Model]]:
        """
        Return the base SELECT query for the model.

        Returns
        -------
        SQLModel.Select
            A SELECT statement targeting the model.
        """
        return select(self.model)

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

    async def delete(self, *, obj: Model) -> None:
        """
        Delete a model instance.

        Parameters
        ----------
        obj
            The model instance to delete.
        """
        await self.session.delete(obj)
        await self.session.commit()

    async def delete_by_id(self, *, id: int) -> None:
        """
        Delete a model instance by primary key.

        Parameters
        ----------
        id
            Primary key of the model.

        Raises
        ------
        NotFoundError
            If the model instance does not exist.
        """
        obj = await self.get_or_raise(id=id)
        await self.delete(obj=obj)

    async def bulk_delete(self, *, ids: Iterable[int]) -> int:
        """
        Delete multiple records by primary key.

        Parameters
        ----------
        ids
            Iterable of primary key values.

        Returns
        -------
        int
            Number of rows deleted.
        """
        stmt = delete(self.model).where(self.model.id.in_(ids))  # type: ignore
        result = await self.session.execute(stmt)
        await self.session.commit()
        return cast(int, result.rowcount) or 0  # type: ignore

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

    async def lock_for_update(self, *, id: int) -> Model:
        """
        Retrieve a record by primary key and lock it for update.

        This issues a SELECT ... FOR UPDATE statement.

        Parameters
        ----------
        id
            Primary key of the model.

        Returns
        -------
        Model
            The locked model instance.

        Raises
        ------
        NotFoundError
            If the model instance does not exist.
        """
        stmt = select(self.model).where(self.model.id == id).with_for_update()  # type: ignore
        obj = (await self.session.execute(stmt)).scalar_one_or_none()

        if not obj:
            raise NotFoundError()

        return obj
