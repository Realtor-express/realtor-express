import uuid
from datetime import datetime, timedelta

from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def default_expires_at():
    return datetime.utcnow() + timedelta(days=7)


class Broadcast(Base):
    __tablename__ = "broadcasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_by_agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    zip_codes: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")  # active / expired / closed
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=default_expires_at, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
