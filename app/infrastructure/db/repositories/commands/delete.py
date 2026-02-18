from typing import Sequence

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..base import BaseCommand

# =============================================================================
# Delete One Record
# =============================================================================


class DeleteOne[T: SQLModel](BaseCommand[int]):
    def __init__(self, *, obj: T) -> None:
        self.obj = obj

    async def execute(self, session: AsyncSession) -> int:
        await session.delete(self.obj)
        return 1


# =============================================================================
# Delete Many Records
# =============================================================================


class DeleteMany[T: SQLModel](BaseCommand[int]):
    def __init__(self, *, objs: Sequence[T]) -> None:
        self.objs = objs

    async def execute(self, session: AsyncSession) -> int:
        for obj in self.objs:
            await session.delete(obj)

        return len(self.objs)
