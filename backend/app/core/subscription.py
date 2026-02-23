from datetime import datetime, timezone

from app.models.agent_profile import AgentProfile


def is_trial_active(profile: AgentProfile) -> bool:
    if not profile.trial_until:
        return False
    return profile.trial_until > datetime.now(timezone.utc)


def has_pro_access(profile: AgentProfile) -> bool:
    """
    Pro access means user can initiate actions (create broadcasts)
    and can see contacts (depending on future rules).
    """
    if profile.subscription_plan in ("pro", "team"):
        return True
    if is_trial_active(profile):
        return True
    return False
