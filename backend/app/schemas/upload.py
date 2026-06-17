from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    id: UUID
    camera_id: UUID | None = None
    image_url: str
    original_filename: str
    content_type: str
    file_size_bytes: int = Field(ge=0)
    processing_status: str
    captured_at: datetime | None = None
    detected_violations: int = Field(ge=0)

