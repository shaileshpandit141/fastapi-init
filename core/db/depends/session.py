from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from ..sessions.session import session


def get_session() -> Generator[Session, None]:
    with session() as sessionx:
        yield sessionx


SessionDep = Annotated[AsyncSession, Depends(get_session)]
