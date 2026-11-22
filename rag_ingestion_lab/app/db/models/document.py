from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import(
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func
)

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


from app.db.base import Base

class Documument(Base):
    __tablename__ = "documents"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_documents_tenant_id",
        ),
    )
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )