from typing import Any, Sequence

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..base import BaseCommand

# =============================================================================
# Select Many Record
# =============================================================================


class SelectOne[T: SQLModel](BaseCommand[T | None]):
    def __init__(
        self,
        *,
        model: type[T],
        where: Sequence[Any] | None = None,
        order_by: Sequence[Any] | None = None,
        options: Sequence[Any] | None = None,
    ) -> None:
        self.model = model
        self.where = where
        self.order_by = order_by
        self.options = options

    async def execute(self, session: AsyncSession) -> T | None:
        stmt = select(self.model)

        if self.where:
            for cond in self.where:
                stmt = stmt.where(cond)

        if self.order_by:
            for ob in self.order_by:
                stmt = stmt.order_by(ob)

        if self.options:
            for opt in self.options:
                stmt = stmt.options(opt)

        return (await session.exec(stmt)).first()


# =============================================================================
# Select Many Records
# =============================================================================


class SelectMany[T: SQLModel](BaseCommand[Sequence[T]]):
    def __init__(
        self,
        *,
        model: type[T],
        where: Sequence[Any] | None = None,
        order_by: Sequence[Any] | None = None,
        options: Sequence[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> None:
        self.model = model
        self.where = where
        self.order_by = order_by
        self.options = options
        self.limit = limit
        self.offset = offset

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        stmt = select(self.model)

        if self.where:
            for cond in self.where:
                stmt = stmt.where(cond)

        if self.order_by:
            for ob in self.order_by:
                stmt = stmt.order_by(ob)

        if self.options:
            for opt in self.options:
                stmt = stmt.options(opt)

        if self.limit is not None:
            stmt = stmt.limit(self.limit)

        if self.offset is not None:
            stmt = stmt.offset(self.offset)

        return (await session.exec(stmt)).all()
