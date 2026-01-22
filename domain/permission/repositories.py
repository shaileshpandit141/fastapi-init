from core.repositories.repository import Repository

from .models import Permission
from .schemas import PermissionCreate, PermissionUpdate

# === Permission Repository ===


class PermissionRepository(Repository[Permission, PermissionCreate, PermissionUpdate]):
    pass
