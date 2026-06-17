from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: dict = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    database: str
    timestamp: datetime


class PaginatedResponse(BaseModel, Generic[T]):
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
    items: list[T]


class CameraSummary(ORMModel):
    id: UUID
    name: str
    location_name: str
    latitude: float
    longitude: float
    road_name: str | None = None


class ImageSummary(ORMModel):
    id: UUID
    image_url: str
    original_filename: str
    content_type: str
    captured_at: datetime | None = None
    uploaded_at: datetime
    processing_status: str

