from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin
from app.models.enums import ViolationStatus, ViolationType


class Violation(Base, TimestampMixin):
    __tablename__ = "violations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    image_id: Mapped[UUID] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), index=True)
    camera_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("cameras.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    violation_type: Mapped[ViolationType] = mapped_column(
        Enum(ViolationType, native_enum=False),
        nullable=False,
        index=True,
    )
    vehicle_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    plate_number: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[ViolationStatus] = mapped_column(
        Enum(ViolationStatus, native_enum=False),
        default=ViolationStatus.PENDING_REVIEW,
        nullable=False,
        index=True,
    )
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    reviewed_by: Mapped[UUID | None] = mapped_column(nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    image: Mapped["UploadedImage"] = relationship(back_populates="violations")
    camera: Mapped["Camera | None"] = relationship(back_populates="violations")
    evidence: Mapped[list["ViolationEvidence"]] = relationship(
        back_populates="violation",
        cascade="all, delete-orphan",
    )


class ViolationEvidence(Base, TimestampMixin):
    __tablename__ = "violation_evidence"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    violation_id: Mapped[UUID] = mapped_column(
        ForeignKey("violations.id", ondelete="CASCADE"),
        index=True,
    )
    evidence_image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    cropped_vehicle_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    annotated_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    violation: Mapped["Violation"] = relationship(back_populates="evidence")

