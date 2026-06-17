from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin
from app.models.enums import ImageProcessingStatus


class UploadedImage(Base, TimestampMixin):
    __tablename__ = "images"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    camera_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("cameras.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    captured_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    processing_status: Mapped[ImageProcessingStatus] = mapped_column(
        Enum(ImageProcessingStatus, native_enum=False),
        default=ImageProcessingStatus.PENDING,
        nullable=False,
        index=True,
    )
    processing_error: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    camera: Mapped["Camera | None"] = relationship(back_populates="images")
    detections: Mapped[list["Detection"]] = relationship(
        back_populates="image",
        cascade="all, delete-orphan",
    )
    ocr_results: Mapped[list["OCRResult"]] = relationship(
        back_populates="image",
        cascade="all, delete-orphan",
    )
    violations: Mapped[list["Violation"]] = relationship(
        back_populates="image",
        cascade="all, delete-orphan",
    )

