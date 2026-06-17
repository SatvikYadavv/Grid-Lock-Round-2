from uuid import UUID

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    id: str
    priority: str = Field(pattern="^(high|medium|low)$")
    title: str
    description: str
    camera_id: UUID | None = None
    camera_name: str | None = None
    location_name: str | None = None
    violation_type: str | None = None
    estimated_impact: str


class RecommendationResponse(BaseModel):
    generated_from_violations: int = Field(ge=0)
    recommendations: list[Recommendation]

