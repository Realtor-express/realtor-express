from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class BroadcastCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=1, max_length=5000)
    zip_codes: list[str] = Field(min_length=1)


class BroadcastOut(BaseModel):
    id: UUID
    created_by_agent_id: UUID
    subject: str
    message: str
    zip_codes: list[str]
    status: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class BroadcastResponseCreate(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class BroadcastResponseOut(BaseModel):
    id: UUID
    broadcast_id: UUID
    agent_id: UUID
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class BroadcastAnalyticsOut(BaseModel):
    id: UUID
    subject: str
    message: str
    zip_codes: list[str]
    status: str
    expires_at: datetime
    created_at: datetime
    responses_count: int

    class Config:
        from_attributes = True
