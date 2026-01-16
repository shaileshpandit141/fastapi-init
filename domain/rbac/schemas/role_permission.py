from core.db.base import NonEmptyUpdateModel
from domain.rbac.models.role_permission import RolePermissionBase

# === Role Permission Schemas ===


class RolePermissionRead(RolePermissionBase):
    pass


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(NonEmptyUpdateModel):
    role_id: int | None = None
    permission_id: int | None = None
