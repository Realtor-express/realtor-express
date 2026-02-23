from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.permissions import (
    require_verified_agent,
    require_broadcast_initiator,
)
from app.db.deps import get_db
from app.models.agent_profile import AgentProfile
from app.models.broadcast import Broadcast
from app.models.broadcast_response import BroadcastResponse
from app.models.user import User
from app.schemas.broadcasts import (
    BroadcastCreate,
    BroadcastOut,
    BroadcastResponseCreate,
    BroadcastResponseOut,
)

router = APIRouter()


def _agent_zip_set(db: Session, user_id) -> set[str]:
    profile = db.query(AgentProfile).filter(AgentProfile.user_id == user_id).first()
    return set(profile.service_zip_codes or []) if profile else set()


# =====================================================
# LIST BROADCASTS (Basic allowed)
# =====================================================
@router.get("", response_model=list[BroadcastOut])
def list_broadcasts(
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    """
    Returns broadcasts matching agent ZIP codes.
    Basic plan can read.
    """
    agent_zips = _agent_zip_set(db, user.id)
    if not agent_zips:
        return []

    items = (
        db.query(Broadcast)
        .order_by(Broadcast.created_at.desc())
        .limit(200)
        .all()
    )

    # MVP filtering in Python
    filtered = [
        b for b in items
        if set(b.zip_codes or []).intersection(agent_zips)
    ]

    return filtered[:50]


# =====================================================
# CREATE BROADCAST (Pro / Team / Trial only)
# =====================================================
@router.post("", response_model=BroadcastOut)
def create_broadcast(
    payload: BroadcastCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_broadcast_initiator),
):
    """
    Only Pro/Team/Trial agents can create broadcasts.
    """
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


# =====================================================
# GET SINGLE BROADCAST
# =====================================================
@router.get("/{broadcast_id}", response_model=BroadcastOut)
def get_broadcast(
    broadcast_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    item = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Broadcast not found")

    return item


# =====================================================
# LIST RESPONSES
# =====================================================
@router.get("/{broadcast_id}/responses", response_model=list[BroadcastResponseOut])
def list_broadcast_responses(
    broadcast_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")

    items = (
        db.query(BroadcastResponse)
        .filter(BroadcastResponse.broadcast_id == broadcast_id)
        .order_by(BroadcastResponse.created_at.desc())
        .limit(200)
        .all()
    )

    return items


# =====================================================
# RESPOND TO BROADCAST (Basic allowed)
# =====================================================
@router.post("/{broadcast_id}/responses", response_model=BroadcastResponseOut)
def respond_broadcast(
    broadcast_id: UUID,
    payload: BroadcastResponseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")

    # Optional: prevent responding to own broadcast
    if str(broadcast.created_by_agent_id) == str(user.id):
        raise HTTPException(
            status_code=400,
            detail="You cannot respond to your own broadcast",
        )

    response = BroadcastResponse(
        broadcast_id=broadcast.id,
        agent_id=user.id,
        message=payload.message,
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    return response
