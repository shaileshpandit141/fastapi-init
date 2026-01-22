from typing import Annotated

from fastapi import Depends

from core.db.depends.async_session import AsyncSessionDep

from ..services.user import UserService

# === User Service Dep ===


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
