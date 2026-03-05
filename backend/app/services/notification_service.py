from sqlalchemy.orm import Session

from app.models.notification import Notification


def create_notification(
    db: Session,
    user_id,
    type: str,
    title: str,
    message: str,
    entity_type: str | None = None,
    entity_id=None,
) -> Notification:
    n = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        entity_type=entity_type,
        entity_id=entity_id,
    )
    db.add(n)
    db.commit()
    db.refresh(n)
    return n
