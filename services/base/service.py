# pyright: reportCallIssue=false

from logging import getLogger
from typing import Any, Sequence

from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlmodel import SQLModel, func, select

from .exceptions import ConflictError, NotFoundError

logger = getLogger(__name__)


class AsyncSessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class AsyncCRUDService[
    Model: DeclarativeMeta, CreateModel: SQLModel, UpdateModel: SQLModel
]:
    def __init__(self, *, session: AsyncSession, model: type[Model]) -> None:
        self.session = session
        self.model = model

    def base_query(self) -> Select[tuple[Model]]:
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

    async def get(self, *, id: int) -> Model | None:
        return await self.session.get(self.model, id)

    async def get_or_raise(self, *, id: int) -> Model:
        obj = await self.get(id=id)

        if not obj:
            raise NotFoundError(f"{self.model.__name__} not found")

        return obj

    async def list(
        self, *, limit: int = 20, offset: int = 0, order_by: Any | None = None
    ) -> Sequence[Model]:
        stmt = self.base_query().limit(limit).offset(offset)
        if order_by is not None:
            stmt = stmt.order_by(order_by)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def paginate(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[Sequence[Model], int]:
        data_stmt = self.base_query().limit(limit).offset(offset)
        count_stmt = select(func.count()).select_from(self.base_query().subquery())

        data = (await self.session.execute(data_stmt)).scalars().all()
        total = (await self.session.execute(count_stmt)).scalar_one()

        return data, total

    async def update(self, *, obj: Model, data: UpdateModel) -> Model:
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(obj, field, value)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def patch(self, *, id: int, data: dict[str, Any]) -> Model:
        obj = await self.get_or_raise(id=id)
        for field, value in data.items():
            setattr(obj, field, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def upsert(self, *, lookup: dict[str, Any], data: dict[str, Any]) -> Model:
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
        await self.session.delete(obj)
        await self.session.commit()
