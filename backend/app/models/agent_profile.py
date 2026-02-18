import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AgentProfile(Base):
    __tablename__ = "agent_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    company: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # ZIP codes where agent provides service
    service_zip_codes: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)

    license_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    license_status: Mapped[str] = mapped_column(String(20), nullable=False, default="under_review")  # under_review/verified/rejected

    subscription_plan: Mapped[str] = mapped_column(String(20), nullable=False, default="free")  # free/pro
    contact_visibility: Mapped[bool] = mapped_column(nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=datetime.utcnow,
    onupdate=datetime.utcnow,
    nullable=False,
)


    user = relationship("User", backref="agent_profile", uselist=False)
