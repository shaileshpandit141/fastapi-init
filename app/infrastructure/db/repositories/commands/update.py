from typing import Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..base import BaseCommand

# =============================================================================
# Update One Record
# =============================================================================


class UpdateOne[T: SQLModel](BaseCommand[T]):
    def __init__(self, *, obj: T, data: BaseModel | SQLModel) -> None:
        self.obj = obj
        self.data = data

    async def execute(self, session: AsyncSession) -> T:
        values = self.data.model_dump(exclude_unset=True)

        for k, v in values.items():
            setattr(self.obj, k, v)

        session.add(self.obj)
        return self.obj


# =============================================================================
# Update Many Records
# =============================================================================


class UpdateMany[T: SQLModel](BaseCommand[Sequence[T]]):
    def __init__(self, *, objs: Sequence[T], data: BaseModel | SQLModel) -> None:
        self.objs = objs
        self.data = data

    async def execute(self, session: AsyncSession) -> Sequence[T]:
        values = self.data.model_dump(exclude_unset=True)

        for obj in self.objs:
            for k, v in values.items():
                setattr(obj, k, v)

            session.add(obj)

        return self.objs
