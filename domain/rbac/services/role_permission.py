from typing import Sequence

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repositories.exceptions import EntityConflictException

from ..models.role_permission import RolePermission
from ..repositories.role_permission import RolePermissionRepository
from ..schemas.role_permission import RolePermissionCreate, RolePermissionUpdate

# === Role Permission Service ===


class RolePermissionService:
    def __init__(self, model: type[RolePermission], session: AsyncSession) -> None:
        self.repo = RolePermissionRepository(model=model, session=session)

    async def create_role_permission(
        self, role_permission_in: RolePermissionCreate
    ) -> RolePermission:
        try:
            role_permission = await self.repo.create(
                data=role_permission_in,
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

    async def delete_role_permission(self, role_id: int) -> None:
        role_permission = await self.get_role_permission(role_id=role_id)
        await self.repo.delete(obj=role_permission)
