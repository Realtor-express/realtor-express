from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.auth_deps import get_current_user
from app.db.deps import get_db
from app.models.user import User
from app.models.agent_profile import AgentProfile
from app.models.verification_request import VerificationRequest
from app.schemas.agent import AgentMeOut, AgentProfileOut, AgentProfileUpdate
from app.schemas.verification import VerificationStatusResponse
from app.utils.storage import save_upload
from app.services.verification_service import create_verification_request, ensure_agent_profile

router = APIRouter()


# =====================================================
# ME (user + profile)
# =====================================================
@router.get("/me", response_model=AgentMeOut)
def me(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agent only")

    # ensure profile exists (MVP)
    ensure_agent_profile(db, user.id)

    # refresh user to include relationship (if needed)
    db.refresh(user)
    return user


# =====================================================
# PROFILE
# =====================================================
@router.get("/profile", response_model=AgentProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agent only")

    profile = ensure_agent_profile(db, user.id)
    return profile


@router.put("/profile", response_model=AgentProfileOut)
def update_profile(
    payload: AgentProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agent only")

    profile = ensure_agent_profile(db, user.id)

    if payload.company is not None:
        profile.company = payload.company

    if payload.service_zip_codes is not None:
        # normalize ZIPs (remove duplicates, trim spaces)
        normalized = []
        for z in payload.service_zip_codes:
            if not z:
                continue
            z = str(z).strip()
            if z and z not in normalized:
                normalized.append(z)
        profile.service_zip_codes = normalized

    db.commit()
    db.refresh(profile)
    return profile


# =====================================================
# VERIFICATION SUBMIT (upload)
# =====================================================
@router.post("/verification", response_model=VerificationStatusResponse)
def submit_verification(
    license_number: str = Form(...),
    license_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agent only")

    document_url = save_upload(license_file, subdir="licenses")

    vr = create_verification_request(
        db=db,
        agent_user_id=user.id,
        license_number=license_number,
        document_url=document_url,
    )
    return vr


@router.get("/verification/status", response_model=VerificationStatusResponse)
def verification_status(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agent only")

    vr = (
        db.query(VerificationRequest)
        .filter(VerificationRequest.agent_id == user.id)
        .order_by(VerificationRequest.created_at.desc())
        .first()
    )
    if not vr:
        raise HTTPException(status_code=404, detail="No verification request found")

    return vr
