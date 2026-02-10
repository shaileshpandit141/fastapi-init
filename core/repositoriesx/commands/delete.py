from typing import Sequence

from sqlmodel import SQLModel

from ..commands import AsyncSession, RepoCommand

# =============================================================================
# Delete Record Command
# =============================================================================


class Delete[T: SQLModel](RepoCommand[int]):
    def __init__(self, objs: Sequence[T]) -> None:
        self.objs = objs

    async def execute(self, session: AsyncSession) -> int:
        for obj in self.objs:
            await session.delete(obj)

        return len(self.objs)
