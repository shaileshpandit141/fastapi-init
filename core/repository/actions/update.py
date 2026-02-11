# update.py
from typing import Sequence

from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..base import BaseAction


class UpdateMany[T: SQLModel](BaseAction[Sequence[T]]):
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
