from click import command, echo
from sqlmodel import select

from core.db.sessions import session
from domain.permission.models import Permission

from .constants import PERMISSIONS

# ===== Seed permissions =====


@command()
def permissions() -> None:
    """Seed all system permissions into the database."""

    with session() as db:
        try:
            existing = {p.code for p in db.exec(select(Permission)).all()}

            for code, description in PERMISSIONS:
                if code not in existing:
                    db.add(
                        Permission(
                            code=code,
                            description=description,
                        )
                    )

            db.commit()
            echo("Permissions seeded successfully.")
        except Exception as exc:
            db.rollback()
            echo(f"Permission seeding failed: {exc}")
            raise
