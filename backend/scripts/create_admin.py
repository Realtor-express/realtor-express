import sys

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def main() -> int:
    email = getattr(settings, "ADMIN_EMAIL", None)
    password = getattr(settings, "ADMIN_PASSWORD", None)

    if not email or not password:
        print("ERROR: ADMIN_EMAIL and ADMIN_PASSWORD must be set in .env")
        return 1

    db: Session = SessionLocal()

    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"Admin already exists: {email}")
            return 0

        admin = User(
            email=email,
            password_hash=hash_password(password),
            first_name="Admin",
            last_name="User",
            role="admin",
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(f"Created admin user: {admin.email} (id={admin.id})")
        return 0

    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
