from typing import cast

from click import command, echo, option
from sqlmodel import select

from core.security.password import hash_password
from db.connections import sessions
from models.role import Role
from models.user import User
from models.user_role_link import UserRoleLink


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
    try:
        with sessions.SyncSessionLocal() as session:
            user = User(email=email, password_hash=hash_password(password))
            session.add(user)
            session.commit()
            session.refresh(user)

            # Featch admin role
            role = session.exec(select(Role).where(Role.name == "admin")).first()
            if role is None:
                echo("Admin role does not exist")
                return

            # Grant to admin role
            session.add(
                UserRoleLink(user_id=cast(int, user.id), role_id=cast(int, role.id))
            )
            session.commit()

            echo("Admin user created successfully.")
    except Exception as err:
        echo(f"Admin user creation failed: {err}")
        pass
