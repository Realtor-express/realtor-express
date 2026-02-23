from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.auth_deps import require_admin
from app.db.deps import get_db
from app.models.agent_profile import AgentProfile
from app.models.user import User
from app.models.verification_request import VerificationRequest
from app.schemas.admin import AdminReviewDecision
from app.schemas.subscription_admin import SetSubscriptionRequest, SetSubscriptionResponse
from app.schemas.verification import VerificationStatusResponse
from app.services.verification_service import set_verification_status

router = APIRouter()


# =====================================================
# VERIFICATION REQUESTS (list + filter + pagination)
# =====================================================
@router.get("/verification-requests")
def list_verification_requests(
    status: str | None = Query(default=None, description="under_review/verified/rejected"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    q = db.query(VerificationRequest)

    if status:
        q = q.filter(VerificationRequest.status == status)

    total = q.count()

    items = (
        q.order_by(VerificationRequest.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset, "status": status}


# =====================================================
# APPROVE / REJECT VERIFICATION
# =====================================================
@router.post("/verification-requests/{request_id}/approve", response_model=VerificationStatusResponse)
def approve_verification(
    request_id: UUID,
    payload: AdminReviewDecision | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    try:
        vr = set_verification_status(
            db=db,
            request_id=request_id,
            admin_id=admin.id,
            status="verified",
            review_note=(payload.review_note if payload else None),
        )
        return vr
    except ValueError:
        raise HTTPException(status_code=404, detail="Request not found")


@router.post("/verification-requests/{request_id}/reject", response_model=VerificationStatusResponse)
def reject_verification(
    request_id: UUID,
    payload: AdminReviewDecision | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    try:
        vr = set_verification_status(
            db=db,
            request_id=request_id,
            admin_id=admin.id,
            status="rejected",
            review_note=(payload.review_note if payload else None),
        )
        return vr
    except ValueError:
        raise HTTPException(status_code=404, detail="Request not found")


# =====================================================
# SUBSCRIPTION MANAGEMENT (Admin)
# =====================================================
@router.post("/agents/{user_id}/subscription", response_model=SetSubscriptionResponse)
def set_agent_subscription(
    user_id: UUID,
    payload: SetSubscriptionRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    plan = (payload.subscription_plan or "").strip().lower()
    if plan not in ("basic", "pro", "team"):
        raise HTTPException(status_code=400, detail="Invalid subscription_plan. Use: basic, pro, team")

    profile = db.query(AgentProfile).filter(AgentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="AgentProfile not found")

    profile.subscription_plan = plan
    profile.trial_until = payload.trial_until  # can be None to clear

    db.commit()
    db.refresh(profile)

    return SetSubscriptionResponse(
        user_id=str(profile.user_id),
        subscription_plan=profile.subscription_plan,
        trial_until=profile.trial_until,
    )
