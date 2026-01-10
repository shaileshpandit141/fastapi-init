# pyright: reportCallIssue=false

from logging import getLogger
from typing import Any, Sequence

from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlmodel import SQLModel, select

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
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        order_by: Any | None = None,
    ) -> Sequence[Model]:
        stmt = self.base_query().limit(limit).offset(offset)
        if order_by is not None:
            stmt = stmt.order_by(order_by)

        result = await self.session.execute(stmt)
        return result.scalars().all()
