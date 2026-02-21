from click import command, echo
from sqlmodel import select

from app.adapters.db.models.role import Role
from app.adapters.db.session import SyncSessionLocal
from app.shared.enums.role import RoleEnum

# =============================================================================
# Role seeder command.
# =============================================================================


@command(name="roles")
def role_command() -> None:
    """Seed roles into the database."""

    with SyncSessionLocal() as session:
        try:
            existing = session.exec(select(Role))
            existing_names = {role.name for role in existing.all()}

            for role in RoleEnum:
                if role not in existing_names:
                    session.add(
                        Role(
                            name=role.value,
                            description=role.label,
                        )
                    )
        except Exception as exc:
            session.rollback()
            echo("Role seeding failed: " + str(exc))
        else:
            session.commit()
            echo("Roles seeded successfully.")
