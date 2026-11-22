
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DocumentVersion(Base):
    __tablename__ = "document_versions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "document_id"],
            ["documents.tenant_id", "documents.id"],
            name="fk_document_versions_document",
        ),
        UniqueConstraint(
            "tenant_id",
            "id",
            name="uq_document_versions_tenant_id",
        ),
        UniqueConstraint(
            "tenant_id",
            "document_id",
            "version_number",
            name="uq_document_versions_number",
        ),
        CheckConstraint(
            "status IN ('pending', 'processing', "
            "'active', 'superseded', 'failed')",
            name="ck_document_versions_status",
        ),
        Index(
            "uq_document_versions_active",
            "tenant_id",
            "document_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    tenant_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
    )
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
    )
    version_number: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(String(64))
    storage_path: Mapped[str] = mapped_column(String(1024))
    status: Mapped[str] = mapped_column(
        String(20),
        server_default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
