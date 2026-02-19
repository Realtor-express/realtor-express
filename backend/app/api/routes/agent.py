from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.auth_deps import get_current_user
from app.db.deps import get_db
from app.models.user import User
from app.models.verification_request import VerificationRequest
from app.schemas.verification import VerificationStatusResponse
from app.utils.storage import save_upload
from app.services.verification_service import create_verification_request

router = APIRouter()


@router.get("/profile")
def get_profile():
    return {"message": "agent profile: TODO"}


@router.put("/profile")
def update_profile():
    return {"message": "update profile: TODO"}


@router.post("/verification", response_model=VerificationStatusResponse)
def submit_verification(
    license_number: str = Form(...),
    license_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agent only")

    # сохраняем файл
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
