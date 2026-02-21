from click import command, echo
from sqlmodel import select

from app.adapters.db.models import Permission
from app.adapters.db.session import SyncSessionLocal
from app.shared.enums.permission import PermissionEnum

# =============================================================================
# Permission seeder command.
# =============================================================================


@command()
def permissions() -> None:
    """Seed permissions into the database."""

    with SyncSessionLocal() as session:
        try:
            existing = session.exec(select(Permission))
            existing_codes = {perm.code for perm in existing.all()}

            for perm in PermissionEnum:
                if perm not in existing_codes:
                    session.add(
                        Permission(
                            code=perm,
                            description=perm.label,
                        )
                    )
        except Exception as exc:
            session.rollback()
            echo("Permission seeding failed: " + str(exc))
        else:
            session.commit()
            echo("Permissions seeded successfully.")
