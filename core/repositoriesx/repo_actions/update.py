from typing import Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel

from .base import AsyncSession, BaseRepoAction

# =============================================================================
# Update One Record Action
# =============================================================================


class UpdateOne[T: SQLModel, D: SQLModel | BaseModel](BaseRepoAction[T]):
    def __init__(self, obj: T, data: D) -> None:
        self.obj = obj
        self.data = data

    async def execute(self, session: AsyncSession) -> T:
        for k, v in self.data.model_dump().items():
            setattr(self.obj, k, v)

        session.add(self.obj)
        await session.commit()
        await session.refresh(self.obj)
        return self.obj


# =============================================================================
# Update Many Record Action
# =============================================================================


class UpdateMany[T: Sequence[SQLModel], D: SQLModel | BaseModel](BaseRepoAction[T]):
    def __init__(self, objs: T, data: D) -> None:
        self.objs = objs
        self.data = data

    async def execute(self, session: AsyncSession) -> T:
        for obj in self.objs:
            for k, v in self.data.model_dump().items():
                setattr(obj, k, v)
            session.add(obj)

        await session.commit()
        for obj in self.objs:
            await session.refresh(obj)

        return self.objs
