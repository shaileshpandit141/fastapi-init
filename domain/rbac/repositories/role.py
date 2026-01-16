from core.repository.base import AsyncRepository

from ..models.role import Role
from ..schemas.role import RoleCreate, RoleUpdate

# === Role Repository ===


class RoleRepository(AsyncRepository[Role, RoleCreate, RoleUpdate]):
    pass
