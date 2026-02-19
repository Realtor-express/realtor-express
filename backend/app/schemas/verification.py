from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class VerificationStatusResponse(BaseModel):
    id: UUID
    agent_id: UUID
    license_number: str
    document_url: str
    status: str
    review_note: str | None = None
    created_at: datetime
    reviewed_at: datetime | None = None
