from typing import Any, Iterable, Sequence

from base.repository import BaseRepository
from sqlmodel import SQLModel, func, select


class ReadRepositoryMixin[Model: SQLModel](BaseRepository[Model]):

    async def get(self, *, id: int) -> Model | None:
        return await self.session.get(self.model, id)

    async def get_by(self, **filters: Any) -> Model | None:
        stmt = self.base_query().filter_by(**filters)
        return (await self.session.exec(stmt)).one_or_none()

    async def list(
        self, *, limit: int = 20, offset: int = 0, order_by: Any | None = None
    ) -> Sequence[Model]:
        stmt = self.base_query().limit(limit).offset(offset)

        if order_by is not None:
            stmt = stmt.order_by(order_by)

        return (await self.session.exec(stmt)).all()

    async def find_by(
        self,
        *,
        conditions: Iterable[Any] | None = None,
        limit: int = 20,
        offset: int = 0,
        order_by: Any | None = None,
    ) -> Sequence[Model]:
        stmt = self.base_query().limit(limit).offset(offset)

        if conditions is not None:
            for condition in conditions:
                stmt = stmt.where(condition)

        if order_by is not None:
            stmt = stmt.order_by(order_by)

        return (await self.session.exec(stmt)).all()

    async def exists(self, **filters: Any) -> bool:
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        return (await self.session.exec(stmt)).one() > 0
