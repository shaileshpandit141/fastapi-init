from click import command, echo
from sqlmodel import select

from core.db.sessions import session
from domain.role.models import Role

from .constants import ROLES

# ===== Seed roles =====


@command()
def roles() -> None:
    """Seed all system roles into the database."""

    with session() as db:
        try:
            existing = {r for r in db.exec(select(Role.name)).all()}

            for name, description in ROLES:
                if name not in existing:
                    db.add(
                        Role(
                            name=name,
                            description=description,
                        )
                    )

            db.commit()
            echo("Roles seeded successfully.")

        except Exception as exc:
            db.rollback()
            echo(f"Role seeding failed: {exc}")
            raise
