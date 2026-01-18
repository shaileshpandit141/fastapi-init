from typing import Sequence

from fastapi import HTTPException, status

from core.db.imports import AsyncSession
from core.repository.exceptions import ConflictError, NotFoundError

from ..models.permission import Permission
from ..repositories.permission import PermissionRepository
from ..schemas.permission import PermissionCreate, PermissionUpdate

# === Permission Service ===


class PermissionService:
    def __init__(self, model: type[Permission], session: AsyncSession) -> None:
        self.permission_repo = PermissionRepository(model=model, session=session)

    async def create_permission(self, permission_in: PermissionCreate) -> Permission:
        try:
            permission = await self.permission_repo.create(data=permission_in)
        except ConflictError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission already exist",
            )

        return permission

    async def get_permission(self, permission_id: int) -> Permission:
        try:
            permission = await self.permission_repo.get_or_raise(id=permission_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission does not exist",
            )

        return permission

    async def list_permission(
        self, limit: int = 20, offset: int = 0
    ) -> Sequence[Permission]:
        permissions = await self.permission_repo.list(
            limit=limit,
            offset=offset,
        )

        return permissions

    async def update_permission(
        self, permission_id: int, permission_in: PermissionUpdate
    ) -> Permission:
        db_permission = await self.get_permission(permission_id)

        permission = await self.permission_repo.update(
            obj=db_permission,
            data=permission_in,
        )

        return permission

    async def delete_permission(self, permission_id: int) -> None:
        try:
            await self.permission_repo.delete_by_id(id=permission_id)
        except NotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission does not exist",
            )
