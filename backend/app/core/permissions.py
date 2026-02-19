from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_deps import get_current_user
from app.db.deps import get_db
from app.models.agent_profile import AgentProfile
from app.models.user import User


def require_verified_agent(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Agent only")

    profile = db.query(AgentProfile).filter(AgentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=403, detail="Profile not found")

    if profile.license_status != "verified":
        raise HTTPException(
            status_code=403,
            detail="Your license must be verified to access this feature",
        )

    return user
