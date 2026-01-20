from typing import Sequence

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repository.exceptions import EntityConflictException, EntityNotFoundException

from ..models.role import Role
from ..repositories.role import RoleRepository
from ..schemas.role import RoleCreate, RoleUpdate

# === Role Service ===


class RoleService:
    def __init__(self, model: type[Role], session: AsyncSession) -> None:
        self.role_repo = RoleRepository(model=model, session=session)

    async def create_role(self, role_in: RoleCreate) -> Role:
        try:
            role = await self.role_repo.create(data=role_in)
        except EntityConflictException:
            raise AlreadyExistsException(detail="Role already exists.")

        return role

    async def get_role(self, role_id: int) -> Role:
        try:
            role = await self.role_repo.get_or_raise(id=role_id)
        except EntityNotFoundException:
            raise NotFoundException(detail="Role not found.")

        return role

    async def list_role(self, limit: int = 20, offset: int = 0) -> Sequence[Role]:
        roles = await self.role_repo.list(
            limit=limit,
            offset=offset,
        )
        return roles

    async def update_role(self, role_id: int, role_in: RoleUpdate) -> Role:
        db_role = await self.get_role(role_id)

        role = await self.role_repo.update(
            obj=db_role,
            data=role_in,
        )

        return role

    async def delete_role(self, role_in: int) -> None:
        try:
            await self.role_repo.delete_by_id(id=role_in)
        except EntityNotFoundException:
            raise NotFoundException(detail="Role not found.")
