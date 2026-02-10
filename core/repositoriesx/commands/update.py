from typing import Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel

from ..commands import AsyncSession, RepoCommand

# =============================================================================
# Update Record Command
# =============================================================================


class Update[T: SQLModel](RepoCommand[Sequence[T]]):
    def __init__(self, objs: Sequence[T], data: BaseModel) -> None:
        self.objs = objs
        self.data = data

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        values = self.data.model_dump(exclude_unset=True)

        for obj in self.objs:
            for k, v in values.items():
                setattr(obj, k, v)
            session.add(obj)

        return self.objs
