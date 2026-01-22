from core.repositories.repository import Repository

from ..models.role import Role
from ..schemas.role import RoleCreate, RoleUpdate

# === Role Repository ===


class RoleRepository(Repository[Role, RoleCreate, RoleUpdate]):
    pass
