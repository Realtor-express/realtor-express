from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.directory_permissions import require_directory_access
from app.db.deps import get_db
from app.models.agent_profile import AgentProfile
from app.models.user import User
from app.schemas.directory import DirectoryAgentOut

router = APIRouter()


@router.get("", response_model=list[DirectoryAgentOut])
def list_agents(
    zip_code: str | None = Query(default=None, description="Filter by ZIP code"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    me: User = Depends(require_directory_access),
):
    """
    Pro/Team/Trial only.
    Returns verified agents directory with contacts visible.
    """
    q = (
        db.query(User, AgentProfile)
        .join(AgentProfile, AgentProfile.user_id == User.id)
        .filter(User.role == "agent")
        .filter(AgentProfile.license_status == "verified")
    )

    if zip_code:
        # MVP: filter in Python (simple). For production use SQL array contains.
        rows = q.all()
        filtered = []
        for u, p in rows:
            if zip_code in (p.service_zip_codes or []):
                filtered.append((u, p))
        rows = filtered[offset: offset + limit]
    else:
        rows = q.order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    result: list[DirectoryAgentOut] = []
    for u, p in rows:
        result.append(
            DirectoryAgentOut(
                user_id=u.id,
                first_name=u.first_name,
                last_name=u.last_name,
                email=u.email,   # contacts visible for Pro access
                phone=u.phone,
                company=p.company,
                service_zip_codes=p.service_zip_codes or [],
                license_status=p.license_status,
                subscription_plan=p.subscription_plan,
                trial_until=p.trial_until,
            )
        )

    return result
