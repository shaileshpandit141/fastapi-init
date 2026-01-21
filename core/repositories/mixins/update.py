from typing import Any

from base.repository import BaseRepository
from pydantic import BaseModel
from sqlmodel import SQLModel


class UpdateRepositoryMixin[Model: SQLModel, UpdateModel: SQLModel | BaseModel](
    BaseRepository[Model]
):
    async def update(self, *, obj: Model, data: UpdateModel) -> Model:
        updates = data.model_dump(exclude_unset=True)

        for k, v in updates.items():
            setattr(obj, k, v)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def patch(self, *, obj: Model, data: dict[str, Any]) -> Model:
        for k, v in data.items():
            setattr(obj, k, v)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj
