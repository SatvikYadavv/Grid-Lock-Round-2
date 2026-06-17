from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class CountByType(BaseModel):
    violation_type: str
    count: int = Field(ge=0)


class CountByStatus(BaseModel):
    status: str
    count: int = Field(ge=0)


class CountByCamera(BaseModel):
    camera_id: UUID | None
    camera_name: str
    location_name: str
    count: int = Field(ge=0)


class TrendPoint(BaseModel):
    date: date
    count: int = Field(ge=0)


class AnalyticsResponse(BaseModel):
    total_violations: int = Field(ge=0)
    pending_review: int = Field(ge=0)
    confirmed: int = Field(ge=0)
    rejected: int = Field(ge=0)
    by_type: list[CountByType]
    by_status: list[CountByStatus]
    by_camera: list[CountByCamera]
    trend: list[TrendPoint]

