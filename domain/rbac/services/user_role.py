from typing import Sequence

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repositories.exceptions import EntityConflictException

from ..models.user_role import UserRole
from ..repositories.user_role import UserRoleRepository
from ..schemas.user_role import UserRoleCreate, UserRoleUpdate

# === User Role Service ===


class UserRoleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRoleRepository(model=UserRole, session=session)

    async def create_user_role(self, user_role_in: UserRoleCreate) -> UserRole:
        try:
            user_role = await self.repo.create(data=user_role_in)
        except EntityConflictException:
            raise AlreadyExistsException(detail="User role already exists.")

        return user_role

    async def get_user_role(self, user_id: int) -> UserRole:
        role = await self.repo.get_by(user_id=user_id)

        if not role:
            raise NotFoundException(detail="User role not found.")

        return role

    async def list_user_roles(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> Sequence[UserRole]:
        roles = await self.repo.find_by(
            conditions=[UserRole.user_id == user_id], limit=limit, offset=offset
        )
        return roles

    async def update_user_role(
        self, user_id: int, user_role_in: UserRoleUpdate
    ) -> UserRole:
        user_role = await self.get_user_role(user_id=user_id)

        user_role = await self.repo.update(obj=user_role, data=user_role_in)

        return user_role

    async def delete_user_role(self, user_id: int) -> None:
        user_role = await self.get_user_role(user_id=user_id)
        await self.repo.delete(obj=user_role)
