from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import require_verified_agent
from app.db.deps import get_db
from app.models.agent_profile import AgentProfile
from app.models.broadcast import Broadcast
from app.models.user import User
from app.schemas.broadcasts import BroadcastCreate, BroadcastOut

router = APIRouter()


def _agent_zip_set(db: Session, user_id) -> set[str]:
    profile = db.query(AgentProfile).filter(AgentProfile.user_id == user_id).first()
    return set(profile.service_zip_codes or []) if profile else set()


@router.get("", response_model=list[BroadcastOut])
def list_broadcasts(
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    # MVP: показываем broadcasts, которые пересекаются с ZIP агента
    agent_zips = _agent_zip_set(db, user.id)
    if not agent_zips:
        return []

    items = (
        db.query(Broadcast)
        .order_by(Broadcast.created_at.desc())
        .limit(200)
        .all()
    )

    # Фильтр пересечения ZIP (быстро для MVP; позже лучше в SQL)
    filtered = [b for b in items if set(b.zip_codes or []).intersection(agent_zips)]
    return filtered[:50]


@router.post("", response_model=BroadcastOut)
def create_broadcast(
    payload: BroadcastCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    broadcast = Broadcast(
        created_by_agent_id=user.id,
        subject=payload.subject,
        message=payload.message,
        zip_codes=payload.zip_codes,
    )

    db.add(broadcast)
    db.commit()
    db.refresh(broadcast)

    return broadcast


@router.get("/{broadcast_id}", response_model=BroadcastOut)
def get_broadcast(
    broadcast_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    item = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
