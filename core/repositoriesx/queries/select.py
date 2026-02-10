from typing import Any, Sequence

from sqlmodel import SQLModel, select

from ..queries import AsyncSession, RepoQuery


class SelectQuery[T: SQLModel](RepoQuery[Sequence[T]]):
    def __init__(
        self,
        model: type[T],
        where: Sequence[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        order_by: Sequence[Any] | None = None,
        options: Sequence[Any] | None = None,
    ) -> None:
        self.model = model
        self.where = where
        self.limit = limit
        self.offset = offset
        self.order_by = order_by
        self.options = options

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        stmt = select(self.model)
        if self.where:
            for cond in self.where:
                stmt = stmt.where(cond)

        if self.order_by:
            for order_by in self.order_by:
                stmt = stmt.order_by(order_by)

        if self.limit:
            stmt = stmt.limit(self.limit)

        if self.offset:
            stmt = stmt.offset(self.offset)

        if self.options:
            for opt in self.options:
                stmt = stmt.options(opt)

        return (await session.exec(stmt)).all()
