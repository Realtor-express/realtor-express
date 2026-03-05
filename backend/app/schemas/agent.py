from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class AgentProfileUpdate(BaseModel):
    company: str | None = Field(default=None, max_length=255)
    service_zip_codes: list[str] | None = Field(default=None, description="ZIP codes where agent operates")
    notifications_enabled: bool | None = Field(default=None, description="Enable/disable notifications")


class AgentProfileOut(BaseModel):
    user_id: UUID
    company: str | None
    service_zip_codes: list[str]
    license_number: str | None
    license_status: str
    subscription_plan: str
    trial_until: datetime | None
    notifications_enabled: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentMeOut(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    phone: str | None

    role: str

    agent_profile: AgentProfileOut | None

    class Config:
        from_attributes = True
