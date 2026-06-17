from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import CameraSummary, ImageSummary, ORMModel, PaginatedResponse


class ViolationEvidenceRead(ORMModel):
    id: UUID
    evidence_image_url: str
    cropped_vehicle_url: str | None = None
    annotated_image_url: str | None = None
    notes: str | None = None


class ViolationRead(ORMModel):
    id: UUID
    image_id: UUID
    camera_id: UUID | None = None
    violation_type: str
    vehicle_type: str | None = None
    plate_number: str | None = None
    confidence: float = Field(ge=0, le=1)
    status: str
    detected_at: datetime
    reviewed_by: UUID | None = None
    reviewed_at: datetime | None = None
    camera: CameraSummary | None = None
    image: ImageSummary
    evidence: list[ViolationEvidenceRead] = Field(default_factory=list)


class ViolationListResponse(PaginatedResponse[ViolationRead]):
    pass


class ViolationFilters(BaseModel):
    violation_type: str | None = None
    status: str | None = None
    camera_id: UUID | None = None
    plate_number: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

