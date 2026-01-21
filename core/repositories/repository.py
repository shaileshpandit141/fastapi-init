from abc import ABC
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

logger = getLogger(__name__)


class BaseRepository[Model: SQLModel](ABC):

    __slots__ = ("model", "session")

    def __init__(self, *, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    def base_query(self) -> SelectOfScalar[Model]:
        return select(self.model)
