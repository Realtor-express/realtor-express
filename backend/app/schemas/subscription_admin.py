from datetime import datetime
from pydantic import BaseModel, Field


class SetSubscriptionRequest(BaseModel):
    subscription_plan: str = Field(description="basic / pro / team")
    trial_until: datetime | None = Field(
        default=None,
        description="Optional trial end datetime (UTC). Use null to clear.",
    )


class SetSubscriptionResponse(BaseModel):
    user_id: str
    subscription_plan: str
    trial_until: datetime | None
