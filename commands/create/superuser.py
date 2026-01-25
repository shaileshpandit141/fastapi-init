from typing import cast

from click import command, echo, option
from sqlmodel import select

from core.db.sessions import session
from core.security.password.hasher import PasswordHasher
from domain.role.constants import RoleType
from domain.role.models import Role
from domain.user.models import User, UserRole


@command()
@option("--email", required=True, help="Email of the user")
@option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password of the user",
)
def superuser(email: str, password: str) -> None:
    """system-level user with unrestricted access and control."""

    hasher = PasswordHasher()

    with session() as db:
        try:
            user = User(
                email=email,
                password_hash=hasher.hash_password(password),
            )  # type: ignore

            db.add(user)
            db.commit()
            db.refresh(user)

            stmt = select(Role.id).where(Role.name == RoleType.SUPERUSER.value)
            role_id = db.exec(stmt).first()

            if not role_id:
                echo("Superuser role does not exist")
                return

            db.add(
                UserRole(
                    user_id=cast(int, user.id),
                    role_id=role_id,
                )
            )
            db.commit()

            echo("Superuser created successfully.")
        except Exception as exc:
            db.rollback()
            echo(f"Superuser creation failed: {exc}", err=True)
