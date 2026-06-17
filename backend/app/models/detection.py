from uuid import UUID, uuid4

from sqlalchemy import Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base, TimestampMixin
from app.models.enums import ObjectType


class Detection(Base, TimestampMixin):
    __tablename__ = "detections"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    image_id: Mapped[UUID] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), index=True)
    object_type: Mapped[ObjectType] = mapped_column(
        Enum(ObjectType, native_enum=False),
        nullable=False,
        index=True,
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_x: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_y: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_width: Mapped[float] = mapped_column(Float, nullable=False)
    bbox_height: Mapped[float] = mapped_column(Float, nullable=False)
    track_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    extra_data: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    image: Mapped["UploadedImage"] = relationship(back_populates="detections")
    ocr_results: Mapped[list["OCRResult"]] = relationship(back_populates="detection")


class OCRResult(Base, TimestampMixin):
    __tablename__ = "ocr_results"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    image_id: Mapped[UUID] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), index=True)
    detection_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("detections.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    plate_number: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    cropped_plate_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    image: Mapped["UploadedImage"] = relationship(back_populates="ocr_results")
    detection: Mapped["Detection | None"] = relationship(back_populates="ocr_results")

