from typing import Sequence

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..base import BaseAction


class DeleteAction[T: SQLModel](BaseAction[int]):
    def __init__(self, objs: Sequence[T]) -> None:
        self.objs = objs

    async def execute(self, session: AsyncSession) -> int:
        for obj in self.objs:
            await session.delete(obj)

        return len(self.objs)
