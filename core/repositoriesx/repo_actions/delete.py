from typing import Any, Sequence

from sqlmodel import SQLModel, delete, select

from .base import AsyncSession, BaseRepoAction

# =============================================================================
# Delete One Record Action
# =============================================================================


class DeleteOne[T: SQLModel](BaseRepoAction[None]):
    def __init__(self, obj: T) -> None:
        self.obj = obj

    async def execute(self, session: AsyncSession) -> None:
        await session.delete(self.obj)
        await session.commit()


class DeleteOnex[T: SQLModel](BaseRepoAction[int]):
    def __init__(self, model: type[T], where: Sequence[Any] | None = None) -> None:
        self.model = model
        self.where = where

    async def execute(self, session: AsyncSession) -> int:
        stmt = select(self.model)
        if self.where:
            for condition in self.where:
                stmt = stmt.where(condition)

        stmt = stmt.limit(1)

        result = await session.exec(stmt)
        row = result.one_or_none()

        if not row:
            return 0

        await session.delete(row)
        await session.commit()

        return 1


# =============================================================================
# Delete Many Record Action
# =============================================================================


class DeleteMany[T: SQLModel](BaseRepoAction[int]):
    def __init__(
        self,
        model: type[T],
        where: Sequence[Any] | None = None,
    ) -> None:
        self.model = model
        self.where = where

    async def execute(self, session: AsyncSession) -> int:
        stmt = delete(self.model)

        if self.where:
            for condition in self.where:
                stmt = stmt.where(condition)

        result = await session.exec(stmt)
        await session.commit()
        return result.rowcount or 0


# =============================================================================
# Delete Many By Ids Record Action
# =============================================================================


class DeleteManyByIds[T: SQLModel](BaseRepoAction[int]):
    def __init__(self, model: type[T], ids: Sequence[int]) -> None:
        self.model = model
        self.ids = ids

    async def execute(self, session: AsyncSession) -> int:
        stmt = delete(self.model).where(self.model.id.in_(self.ids))  # type: ignore
        result = await session.exec(stmt)
        await session.commit()
        return result.rowcount or 0
