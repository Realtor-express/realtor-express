from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import require_verified_agent, require_broadcast_initiator
from app.db.deps import get_db
from app.models.agent_profile import AgentProfile
from app.models.broadcast import Broadcast
from app.models.broadcast_response import BroadcastResponse
from app.models.user import User
from app.schemas.broadcasts import (
    BroadcastAnalyticsOut,
    BroadcastCreate,
    BroadcastOut,
    BroadcastResponseCreate,
    BroadcastResponseOut,
)
from app.services.notification_service import create_notification

router = APIRouter()


def _agent_zip_set(db: Session, user_id) -> set[str]:
    profile = db.query(AgentProfile).filter(AgentProfile.user_id == user_id).first()
    return set(profile.service_zip_codes or []) if profile else set()


def _notify_agents_for_broadcast(db: Session, broadcast: Broadcast) -> None:
    """
    Notify verified agents whose service ZIP codes intersect broadcast ZIP codes.
    Respects AgentProfile.notifications_enabled.
    Excludes the author.
    """
    target_zips = set(broadcast.zip_codes or [])
    if not target_zips:
        return

    profiles = (
        db.query(AgentProfile)
        .filter(AgentProfile.license_status == "verified")
        .filter(AgentProfile.notifications_enabled == True)  # noqa: E712
        .all()
    )

    for p in profiles:
        if str(p.user_id) == str(broadcast.created_by_agent_id):
            continue

        agent_zips = set(p.service_zip_codes or [])
        if agent_zips.intersection(target_zips):
            create_notification(
                db=db,
                user_id=p.user_id,
                type="broadcast_created",
                title="New broadcast in your area",
                message=f"{broadcast.subject}",
                entity_type="broadcast",
                entity_id=broadcast.id,
            )


def _notify_author_for_response(db: Session, broadcast: Broadcast, responder: User) -> None:
    """
    Notify broadcast author that someone responded.
    Respects AgentProfile.notifications_enabled.
    """
    if str(broadcast.created_by_agent_id) == str(responder.id):
        return

    author_profile = db.query(AgentProfile).filter(AgentProfile.user_id == broadcast.created_by_agent_id).first()
    if not author_profile or not author_profile.notifications_enabled:
        return

    create_notification(
        db=db,
        user_id=broadcast.created_by_agent_id,
        type="broadcast_response",
        title="New response to your broadcast",
        message=f"{responder.first_name} {responder.last_name} responded to: {broadcast.subject}",
        entity_type="broadcast",
        entity_id=broadcast.id,
    )


@router.get("", response_model=list[BroadcastOut])
def list_broadcasts(
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    agent_zips = _agent_zip_set(db, user.id)
    if not agent_zips:
        return []

    items = (
        db.query(Broadcast)
        .order_by(Broadcast.created_at.desc())
        .limit(200)
        .all()
    )

    filtered = [
        b for b in items
        if set(b.zip_codes or []).intersection(agent_zips)
    ]

    return filtered[:50]


@router.get("/mine", response_model=list[BroadcastAnalyticsOut])
def my_broadcasts(
    db: Session = Depends(get_db),
    user: User = Depends(require_verified_agent),
):
    items = (
        db.query(Broadcast)
        .filter(Broadcast.created_by_agent_id == user.id)
        .order_by(Broadcast.created_at.desc())
        .limit(200)
        .all()
    )

    result: list[BroadcastAnalyticsOut] = []

    for b in items:
        responses_count = (
            db.query(BroadcastResponse)
            .filter(BroadcastResponse.broadcast_id == b.id)
            .count()
        )

        result.append(
            BroadcastAnalyticsOut(
                id=b.id,
                subject=b.subject,
                message=b.message,
                zip_codes=b.zip_codes or [],
                created_at=b.created_at,
                responses_count=responses_count,
            )
        )

    return result


@router.post("", response_model=BroadcastOut)
def create_broadcast(
    payload: BroadcastCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_broadcast_initiator),
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

    _notify_agents_for_broadcast(db, broadcast)

    return broadcast


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

    if str(broadcast.created_by_agent_id) == str(user.id):
        raise HTTPException(status_code=400, detail="You cannot respond to your own broadcast")

    response = BroadcastResponse(
        broadcast_id=broadcast.id,
        agent_id=user.id,
        message=payload.message,
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    _notify_author_for_response(db, broadcast, user)

    return response
