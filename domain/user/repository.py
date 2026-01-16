from core.repository.base import AsyncRepository

from .models import User
from .schemas import UserCreate, UserUpdate

# === User Repository ===


class UserRepository(AsyncRepository[User, UserCreate, UserUpdate]):
    pass
