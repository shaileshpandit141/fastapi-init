from core.repositories.repository import Repository

from .models import Role, RolePermission
from .schemas import RoleCreate, RolePermissionCreate, RolePermissionUpdate, RoleUpdate

# === Role Repository ===


class RoleRepository(Repository[Role, RoleCreate, RoleUpdate]):
    pass


# === Role Permission Repository ===


class RolePermissionRepository(
    Repository[RolePermission, RolePermissionCreate, RolePermissionUpdate]
):
    pass
