from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password


def register_user(db: Session, email: str, password: str, first_name: str, last_name: str):
    user = User(
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        role="agent",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
