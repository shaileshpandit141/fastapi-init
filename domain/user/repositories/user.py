from core.repository.base import AsyncRepository

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

# === User Repository ===


class UserRepository(AsyncRepository[User, UserCreate, UserUpdate]):
    pass
