from typing import Sequence

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repositories.exceptions import EntityConflictException

from ..models.role import Role
from ..repositories.role import RoleRepository
from ..schemas.role import RoleCreate, RoleUpdate

# === Role Service ===


class RoleService:
    def __init__(self, model: type[Role], session: AsyncSession) -> None:
        self.repo = RoleRepository(model=model, session=session)

    async def create_role(self, role_in: RoleCreate) -> Role:
        try:
            role = await self.repo.create(data=role_in)
        except EntityConflictException:
            raise AlreadyExistsException(detail="Role already exists.")

        return role

    async def get_role(self, role_id: int) -> Role:
        role = await self.repo.get(id=role_id)

        if not role:
            raise NotFoundException(detail="Role not found.")

        return role

    async def list_role(self, limit: int = 20, offset: int = 0) -> Sequence[Role]:
        roles = await self.repo.list(limit=limit, offset=offset)
        return roles

    async def update_role(self, role_id: int, role_in: RoleUpdate) -> Role:
        role = await self.get_role(role_id)

        role = await self.repo.update(obj=role, data=role_in)

        return role

    async def delete_role(self, role_in: int) -> None:
        role = await self.get_role(role_id=role_in)
        await self.repo.delete(obj=role)
