from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import require_verified_agent
from app.db.deps import get_db
from app.models.agent_profile import AgentProfile
from app.models.user import User
from app.schemas.directory import PublicAgentOut

router = APIRouter()


@router.get("/agents/{user_id}", response_model=PublicAgentOut)
def get_public_agent_profile(
    user_id: UUID,
    db: Session = Depends(get_db),
    me: User = Depends(require_verified_agent),
):
    """
    Verified agents can view public profile of other verified agents.
    Contacts are not included here.
    """
    u = db.query(User).filter(User.id == user_id, User.role == "agent").first()
    if not u:
        raise HTTPException(status_code=404, detail="Agent not found")

    p = db.query(AgentProfile).filter(AgentProfile.user_id == u.id).first()
    if not p or p.license_status != "verified":
        raise HTTPException(status_code=404, detail="Agent not found")

    return PublicAgentOut(
        user_id=u.id,
        first_name=u.first_name,
        last_name=u.last_name,
        company=p.company,
        service_zip_codes=p.service_zip_codes or [],
        license_status=p.license_status,
    )
