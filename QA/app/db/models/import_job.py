from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.models.enums import DuplicateStrategy, ImportItemStatus, ImportStatus, SourceType


class ImportJob(TimestampMixin, Base):
    __tablename__ = "import_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_type: Mapped[SourceType] = mapped_column(
        SAEnum(SourceType, native_enum=False, length=20), nullable=False
    )
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[ImportStatus] = mapped_column(
        SAEnum(ImportStatus, native_enum=False, length=20),
        nullable=False,
        default=ImportStatus.PENDING,
    )
    dry_run: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    duplicate_strategy: Mapped[DuplicateStrategy] = mapped_column(
        SAEnum(DuplicateStrategy, native_enum=False, length=20),
        nullable=False,
        default=DuplicateStrategy.SKIP,
    )
    summary_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    warnings_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    errors_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    items: Mapped[list[ImportItem]] = relationship(
        back_populates="import_job", cascade="all, delete-orphan"
    )


class ImportItem(Base):
    __tablename__ = "import_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_job_id: Mapped[int] = mapped_column(
        ForeignKey("import_jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_order: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_data_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ImportItemStatus] = mapped_column(
        SAEnum(ImportItemStatus, native_enum=False, length=20), nullable=False
    )
    question_id: Mapped[int | None] = mapped_column(
        ForeignKey("questions.id", ondelete="SET NULL"), nullable=True
    )
    warnings_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    errors_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    import_job: Mapped[ImportJob] = relationship(back_populates="items")
