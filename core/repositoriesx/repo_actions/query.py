from typing import Any, Sequence

from sqlmodel import SQLModel, select

from .base import AsyncSession, BaseRepoAction

# =============================================================================
# Get One Record Action
# =============================================================================


class GetOne[T: SQLModel](BaseRepoAction[T | None]):
    def __init__(self, model: type[T], where: Sequence[Any]) -> None:
        self.model = model
        self.where = where

    async def execute(self, session: AsyncSession) -> T | None:
        stmt = select(self.model)

        if self.where:
            for condition in self.where:
                stmt = stmt.where(condition)

        result = await session.exec(stmt)

        return result.first()


# =============================================================================
# Get Many Record Action
# =============================================================================


class GetMany[T: SQLModel](BaseRepoAction[Sequence[T]]):
    def __init__(
        self,
        model: type[T],
        *,
        where: Sequence[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Any = None,
    ) -> None:
        self.model = model
        self.where = where
        self.limit = limit
        self.offset = offset
        self.order_by = order_by

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        stmt = select(self.model)

        if self.where is not None:
            for condition in self.where:
                stmt = stmt.where(condition)

        if self.order_by is not None:
            stmt = stmt.order_by(self.order_by)

        if self.limit:
            stmt = stmt.limit(self.limit)
        if self.offset:
            stmt = stmt.offset(self.offset)

        result = await session.exec(stmt)
        return result.all()


# =============================================================================
# Exists Record Action
# =============================================================================


class Exists[T: SQLModel](BaseRepoAction[bool]):
    def __init__(self, model: type[T], where: Sequence[Any]) -> None:
        self.model = model
        self.where = where

    async def execute(self, session: AsyncSession) -> bool:
        stmt = select(self.model)

        if self.where:
            for condition in self.where:
                stmt = stmt.where(condition)

        result = await session.exec(stmt.limit(1))
        return result.first() is not None
