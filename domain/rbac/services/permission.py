from typing import Sequence

from core.db.imports import AsyncSession
from core.exceptions import AlreadyExistsException, NotFoundException
from core.repositories.exceptions import EntityConflictException

from ..models.permission import Permission
from ..repositories.permission import PermissionRepository
from ..schemas.permission import PermissionCreate, PermissionUpdate

# === Permission Service ===


class PermissionService:
    def __init__(self, model: type[Permission], session: AsyncSession) -> None:
        self.repo = PermissionRepository(model=model, session=session)

    async def create_permission(self, permission_in: PermissionCreate) -> Permission:
        try:
            permission = await self.repo.create(data=permission_in)
        except EntityConflictException:
            raise AlreadyExistsException(detail="Permission already exists.")

        return permission

    async def get_permission(self, permission_id: int) -> Permission:
        permission = await self.repo.get(id=permission_id)

        if not permission:
            raise NotFoundException(detail="Permission not found.")

        return permission

    async def list_permission(
        self, limit: int = 20, offset: int = 0
    ) -> Sequence[Permission]:
        permissions = await self.repo.list(
            limit=limit, offset=offset, order_by=Permission.id
        )

        return permissions

    async def update_permission(
        self, permission_id: int, permission_in: PermissionUpdate
    ) -> Permission:
        db_permission = await self.get_permission(permission_id)

        permission = await self.repo.update(
            obj=db_permission,
            data=permission_in,
        )

        return permission

    async def delete_permission(self, permission_id: int) -> None:
        perm = await self.get_permission(permission_id=permission_id)

        await self.repo.delete(obj=perm)
