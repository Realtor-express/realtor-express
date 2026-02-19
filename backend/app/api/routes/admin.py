from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_deps import require_admin
from app.db.deps import get_db
from app.models.user import User
from app.models.verification_request import VerificationRequest
from app.schemas.verification import VerificationStatusResponse
from app.services.verification_service import set_verification_status

router = APIRouter()


@router.get("/verification-requests")
def list_verification_requests(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    items = (
        db.query(VerificationRequest)
        .order_by(VerificationRequest.created_at.desc())
        .limit(200)
        .all()
    )
    return items


@router.post("/verification-requests/{request_id}/approve", response_model=VerificationStatusResponse)
def approve_verification(
    request_id: str,
    body: dict | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    review_note = (body or {}).get("review_note")
    try:
        vr = set_verification_status(db, request_id, admin.id, "verified", review_note)
        return vr
    except ValueError:
        raise HTTPException(status_code=404, detail="Request not found")


@router.post("/verification-requests/{request_id}/reject", response_model=VerificationStatusResponse)
def reject_verification(
    request_id: str,
    body: dict | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    review_note = (body or {}).get("review_note")
    try:
        vr = set_verification_status(db, request_id, admin.id, "rejected", review_note)
        return vr
    except ValueError:
        raise HTTPException(status_code=404, detail="Request not found")
