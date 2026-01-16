from core.repository.base import AsyncRepository

from ..models.role_permission import RolePermission
from ..schemas.role_permission import RolePermissionCreate, RolePermissionUpdate

# === Role Permission Repository ===


class RolePermissionRepository(
    AsyncRepository[RolePermission, RolePermissionCreate, RolePermissionUpdate]
):
    pass
