from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import require_verified_agent
from app.db.deps import get_db
from app.models.broadcast import Broadcast
from app.models.user import User

router = APIRouter()


@router.get("")
def list_broadcasts(
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    # MVP: пока просто возвращаем последние 50
    items = (
        db.query(Broadcast)
        .order_by(Broadcast.created_at.desc())
        .limit(50)
        .all()
    )
    return items


@router.post("")
def create_broadcast(
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    subject = payload.get("subject")
    message = payload.get("message")
    zip_codes = payload.get("zip_codes")

    if not subject or not message or not zip_codes:
        raise HTTPException(status_code=400, detail="Missing required fields")

    broadcast = Broadcast(
        created_by_agent_id=user.id,
        subject=subject,
        message=message,
        zip_codes=zip_codes,
    )

    db.add(broadcast)
    db.commit()
    db.refresh(broadcast)

    return broadcast


@router.get("/{broadcast_id}")
def get_broadcast(
    broadcast_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    item = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")

    return item


@router.post("/{broadcast_id}/responses")
def respond_broadcast(
    broadcast_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    return {"message": "TODO respond broadcast"}

