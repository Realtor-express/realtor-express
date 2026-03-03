from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class DirectoryAgentOut(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    email: str | None
    phone: str | None

    company: str | None
    service_zip_codes: list[str]

    license_status: str
    subscription_plan: str
    trial_until: datetime | None

    class Config:
        from_attributes = True


class PublicAgentOut(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    company: str | None
    service_zip_codes: list[str]
    license_status: str

    class Config:
        from_attributes = True
