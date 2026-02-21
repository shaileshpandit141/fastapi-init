import questionary
from click import command, echo, option
from sqlmodel import select

from app.adapters.db.models.role import Role
from app.adapters.db.models.user import User
from app.adapters.db.models.user_role import UserRole
from app.adapters.db.session import SyncSessionLocal
from app.adapters.security.password.hasher import PasswordHasher
from app.shared.enums.user import UserStatusEnum

# =============================================================================
# Create user command.
# =============================================================================


@command()
@option("--email", required=True, help="Email of the user")
@option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password of the user",
)
def create_user_command(email: str, password: str) -> None:
    """
    Create a new user with the given role.
    """

    hasher = PasswordHasher()

    with SyncSessionLocal() as session:
        try:
            # Check if the email is already in use.
            existing_user = session.exec(
                select(User).where(User.email == email)
            ).first()

            if existing_user:
                raise ValueError("Email is already in use.")

            # Select all available roles from the database.
            role_names = session.exec(select(Role.id, Role.name)).all()

            # Ask the user to select a role.
            selected_role = questionary.select(
                "Choose a role for the user:",
                choices=[role_name for _, role_name in role_names],
            ).ask()

            # Create the user with the selected role.
            user = User(
                email=email,
                password_hash=hasher.hash_password(password),
                status=UserStatusEnum.ACTIVE,
            )

            user.mark_email_verified()
            session.add(user)
            session.flush()  # Flush to get the user ID.

            # Assign the selected role to the user.
            user_role = UserRole(
                user_id=user.id,
                role_id=next(id for id, name in role_names if name == selected_role),
            )

            session.add(user_role)
        except Exception as exc:
            session.rollback()
            echo("User creation failed: " + str(exc))
        else:
            session.commit()
            echo("User created successfully.")
