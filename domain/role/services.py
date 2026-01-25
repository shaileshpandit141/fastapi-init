from typing import Sequence

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import AlreadyExistsException, NotFoundException
from core.repositories.exceptions import EntityConflictException

from .models import Role, RolePermission
from .repositories import RolePermissionRepository, RoleRepository
from .schemas import RoleCreate, RolePermissionCreate, RolePermissionUpdate, RoleUpdate

# === Role Service ===


class RoleService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = RoleRepository(model=Role, session=session)

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

    async def list_roles(self, limit: int = 20, offset: int = 0) -> Sequence[Role]:
        roles = await self.repo.list(limit=limit, offset=offset)
        return roles

    async def update_role(self, role_id: int, role_in: RoleUpdate) -> Role:
        role = await self.get_role(role_id)

        role = await self.repo.update(obj=role, data=role_in)

        return role

    async def delete_role(self, role_id: int) -> None:
        role = await self.get_role(role_id=role_id)
        await self.repo.delete(obj=role)


# === Role Permission Service ===


class RolePermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = RolePermissionRepository(model=RolePermission, session=session)

    async def create_role_permission(
        self, role_id: int, role_permission_in: RolePermissionCreate
    ) -> RolePermission:
        try:
            role_permission = await self.repo.create(
                data=role_permission_in, values={"role_id": role_id}
            )
        except EntityConflictException:
            raise AlreadyExistsException(detail="Role or Permission already exists.")

        return role_permission

    async def get_role_permission(self, role_id: int) -> RolePermission:

        role_permission = await self.repo.get_by(role_id=role_id)

        if not role_permission:
            raise NotFoundException(detail="Role permission not found.")

        return role_permission

    async def list_role_permission(
        self, role_id: int, limit: int = 20, offset: int = 0
    ) -> Sequence[RolePermission]:
        role_permissions = await self.repo.find_by(
            conditions=[RolePermission.role_id == role_id], limit=limit, offset=offset
        )

        return role_permissions

    async def update_role_permission(
        self, role_id: int, role_permission_in: RolePermissionUpdate
    ) -> RolePermission:
        role_permission = await self.get_role_permission(role_id=role_id)

        role_permission = await self.repo.update(
            obj=role_permission, data=role_permission_in
        )

        return role_permission

    async def delete_role_permission(self, role_id: int, permission_id: int) -> None:

        role_perm = await self.repo.get_by(role_id=role_id, permission_id=permission_id)

        if not role_perm:
            raise NotFoundException(detail="Role Permission does not exists")

        await self.repo.delete(obj=role_perm)
