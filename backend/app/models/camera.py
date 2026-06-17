from uuid import UUID, uuid4

from sqlalchemy import Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base, TimestampMixin
from app.models.enums import CameraStatus, ZoneType


class Camera(Base, TimestampMixin):
    __tablename__ = "cameras"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    road_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[CameraStatus] = mapped_column(
        Enum(CameraStatus, native_enum=False),
        default=CameraStatus.ACTIVE,
        nullable=False,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    zones: Mapped[list["CameraZone"]] = relationship(
        back_populates="camera",
        cascade="all, delete-orphan",
    )
    images: Mapped[list["UploadedImage"]] = relationship(back_populates="camera")
    violations: Mapped[list["Violation"]] = relationship(back_populates="camera")


class CameraZone(Base, TimestampMixin):
    __tablename__ = "camera_zones"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    camera_id: Mapped[UUID] = mapped_column(ForeignKey("cameras.id", ondelete="CASCADE"), index=True)
    zone_type: Mapped[ZoneType] = mapped_column(
        Enum(ZoneType, native_enum=False),
        nullable=False,
        index=True,
    )
    polygon_coordinates: Mapped[list[dict[str, float]]] = mapped_column(JSON, nullable=False)
    allowed_direction_angle: Mapped[float | None] = mapped_column(Float, nullable=True)
    extra_data: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)

    camera: Mapped["Camera"] = relationship(back_populates="zones")

