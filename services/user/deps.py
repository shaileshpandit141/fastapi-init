from typing import Annotated

from fastapi import Depends

from dependencies.connections.sessions import AsyncSessionDep

from .service import UserService


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
