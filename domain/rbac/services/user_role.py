from typing import Sequence

from fastapi import HTTPException, status

from core.db import AsyncSession
from core.repository.exceptions import ConflictError, NotFoundError

from ..models.user_role import UserRole
from ..repositories.user_role import UserRoleRepository
from ..schemas.user_role import UserRoleCreate, UserRoleUpdate

# === User Role Service ===


class UserRoleService:
    def __init__(self, model: type[UserRole], session: AsyncSession) -> None:
        self.user_role_repo = UserRoleRepository(model=model, session=session)

    async def create_user_role(self, user_role_in: UserRoleCreate) -> UserRole:
        try:
            user_role = await self.user_role_repo.create(
                data=user_role_in,
            )
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User role already exist",
            )

        return user_role

    async def get_user_role(self, user_role_id: int) -> UserRole:
        try:
            user_role = await self.user_role_repo.get_or_raise(id=user_role_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User role does not exist",
            )

        return user_role

    async def list_user_role(
        self, limit: int = 20, offset: int = 0
    ) -> Sequence[UserRole]:
        user_roles = await self.user_role_repo.list(
            limit=limit,
            offset=offset,
        )

        return user_roles

    async def update_user_role(
        self, user_role_id: int, user_role_in: UserRoleUpdate
    ) -> UserRole:
        db_user_role = await self.get_user_role(user_role_id)

        user_role = await self.user_role_repo.update(
            obj=db_user_role,
            data=user_role_in,
        )

        return user_role

    async def delete_user_role(self, user_role_id: int) -> None:
        try:
            await self.user_role_repo.delete_by_id(id=user_role_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User role does not exist",
            )
