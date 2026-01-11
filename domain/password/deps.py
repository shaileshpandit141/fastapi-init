from typing import Annotated

from fastapi import Depends

from .service import PasswordService


async def get_password_service() -> PasswordService:
    return PasswordService()


PasswordServiceDep = Annotated[PasswordService, Depends(get_password_service)]
