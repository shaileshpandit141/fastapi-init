from core.repositories.repository import Repository

from ..models.permission import Permission
from ..schemas.permission import PermissionCreate, PermissionUpdate

# === Permission Repository ===


class PermissionRepository(Repository[Permission, PermissionCreate, PermissionUpdate]):
    pass
