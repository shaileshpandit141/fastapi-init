from typing import Sequence

from sqlmodel import select

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repository.exceptions import EntityConflictException, EntityNotFoundException

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
        except EntityConflictException:
            raise AlreadyExistsException(detail="User role already exists.")

        return user_role

    async def get_user_role(self, user_role_id: int) -> UserRole:
        try:
            user_role = await self.user_role_repo.get_or_raise(id=user_role_id)
        except EntityNotFoundException:
            raise NotFoundException(detail="User role not found.")

        return user_role

    async def list_user_roles(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> Sequence[UserRole]:
        # stmt = select(UserRole).where(UserRole.user_id == user_id)

        user_roles = await self.user_role_repo.filter(
            where=[UserRole.user_id == user_id],
            limit=limit,
            offset=offset,
        )

        # user_roles = await self.user_role_repo.list(
        #     limit=limit,
        #     offset=offset,
        # )

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
        except EntityNotFoundException:
            raise NotFoundException(detail="User role not found.")
