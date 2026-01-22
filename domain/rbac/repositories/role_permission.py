from core.repositories.repository import Repository

from ..models.role_permission import RolePermission
from ..schemas.role_permission import RolePermissionCreate, RolePermissionUpdate

# === Role Permission Repository ===


class RolePermissionRepository(
    Repository[RolePermission, RolePermissionCreate, RolePermissionUpdate]
):
    pass
