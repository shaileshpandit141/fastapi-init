from typing import Sequence

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repository.exceptions import EntityConflictException, EntityNotFoundException

from ..models.role_permission import RolePermission
from ..repositories.role_permission import RolePermissionRepository
from ..schemas.role_permission import RolePermissionCreate, RolePermissionUpdate

# === Role Permission Service ===


class RolePermissionService:
    def __init__(self, model: type[RolePermission], session: AsyncSession) -> None:
        self.role_permission_repo = RolePermissionRepository(
            model=model, session=session
        )

    async def create_role_permission(
        self, role_permission_in: RolePermissionCreate
    ) -> RolePermission:
        try:
            role_permission = await self.role_permission_repo.create(
                data=role_permission_in,
            )
        except EntityConflictException:
            raise AlreadyExistsException(resource="Role")

        return role_permission

    async def get_role_permission(self, role_permission_id: int) -> RolePermission:
        try:
            role_permission = await self.role_permission_repo.get_or_raise(
                id=role_permission_id
            )
        except EntityNotFoundException:
            raise NotFoundException(resource="Role permission")

        return role_permission

    async def list_role_permission(
        self, limit: int = 20, offset: int = 0
    ) -> Sequence[RolePermission]:
        role_permissions = await self.role_permission_repo.list(
            limit=limit,
            offset=offset,
        )

        return role_permissions

    async def update_role_permission(
        self, role_permission_id: int, role_permission_in: RolePermissionUpdate
    ) -> RolePermission:
        db_role_permission = await self.get_role_permission(role_permission_id)

        role_permission = await self.role_permission_repo.update(
            obj=db_role_permission,
            data=role_permission_in,
        )

        return role_permission

    async def delete_role_permission(self, role_permission_id: int) -> None:
        try:
            await self.role_permission_repo.delete_by_id(id=role_permission_id)
        except EntityNotFoundException:
            raise NotFoundException(resource="Role permission")
