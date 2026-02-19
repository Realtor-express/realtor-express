from datetime import datetime
from sqlalchemy.orm import Session

from app.models.agent_profile import AgentProfile
from app.models.verification_request import VerificationRequest


def ensure_agent_profile(db: Session, user_id):
    profile = db.query(AgentProfile).filter(AgentProfile.user_id == user_id).first()
    if not profile:
        profile = AgentProfile(user_id=user_id, service_zip_codes=[])
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def create_verification_request(
    db: Session,
    agent_user_id,
    license_number: str,
    document_url: str,
) -> VerificationRequest:
    # создаём/находим профиль
    profile = ensure_agent_profile(db, agent_user_id)

    # обновляем профиль
    profile.license_number = license_number
    profile.license_status = "under_review"

    # создаём запрос на верификацию
    vr = VerificationRequest(
        agent_id=agent_user_id,
        license_number=license_number,
        document_url=document_url,
        status="under_review",
    )
    db.add(vr)
    db.commit()
    db.refresh(vr)
    return vr


def set_verification_status(
    db: Session,
    request_id,
    admin_id,
    status: str,
    review_note: str | None = None,
) -> VerificationRequest:
    vr = db.query(VerificationRequest).filter(VerificationRequest.id == request_id).first()
    if not vr:
        raise ValueError("not_found")

    vr.status = status
    vr.review_note = review_note
    vr.reviewed_by_admin_id = admin_id
    vr.reviewed_at = datetime.utcnow()

    # синхронизируем статус в профиле
    profile = db.query(AgentProfile).filter(AgentProfile.user_id == vr.agent_id).first()
    if profile:
        profile.license_status = status

    db.commit()
    db.refresh(vr)
    return vr
