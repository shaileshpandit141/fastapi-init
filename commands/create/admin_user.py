from typing import cast

from click import command, echo, option
from sqlmodel import select

from core.db.sessions import session
from core.security.password.hasher import PasswordHasher
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
def admin_user(email: str, password: str) -> None:
    """Create admin user with email and password"""

    hasher = PasswordHasher()

    try:
        with session() as sessionx:
            user = User(
                email=email,
                password_hash=hasher.hash_password(password),
            )  # type: ignore
            sessionx.add(user)
            sessionx.commit()
            sessionx.refresh(user)

            # Featch admin role
            role = sessionx.exec(select(Role).where(Role.name == "admin")).first()
            if role is None:
                echo("Admin role does not exist")
                return

            # Grant to admin role
            sessionx.add(
                UserRole(user_id=cast(int, user.id), role_id=cast(int, role.id))
            )
            sessionx.commit()

            echo("Admin user created successfully.")
    except Exception as err:
        echo(f"Admin user creation failed: {err}")
        pass
