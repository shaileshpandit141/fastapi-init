from core.repository.base import AsyncRepository

from ..models.permission import Permission
from ..schemas.permission import PermissionCreate, PermissionUpdate

# === Permission Repository ===


class PermissionRepository(
    AsyncRepository[Permission, PermissionCreate, PermissionUpdate]
):
    pass
