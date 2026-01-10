from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlmodel import SQLModel, select


class AsyncSessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class AsyncCRUDService[
    Model: DeclarativeMeta, CreateModel: SQLModel, UpdateModel: SQLModel
]:
    def __init__(self, *, session: AsyncSession, model: type[Model]) -> None:
        self.session = session
        self.model = model

    def base_query(self) -> Select[tuple[Model]]:
        return select(self.model)
