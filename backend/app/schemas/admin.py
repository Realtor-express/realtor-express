from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
    status: str | None = None  # under_review/verified/rejected


class AdminReviewDecision(BaseModel):
    review_note: str | None = Field(default=None, max_length=500)
