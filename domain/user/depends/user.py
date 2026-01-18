from typing import Annotated

from fastapi import Depends

from core.db.depends import AsyncSessionDep

from ..models.user import User
from ..services.user import UserService

# === User Service Dep ===


async def get_user_service(session: AsyncSessionDep) -> UserService:
    return UserService(model=User, session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
