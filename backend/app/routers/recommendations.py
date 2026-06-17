from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_service import RecommendationService


router = APIRouter(tags=["recommendations"])


@router.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    days: int = Query(default=30, ge=1, le=365),
    min_violation_count: int = Query(default=3, ge=1, le=100),
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    return RecommendationService.get_recommendations(
        db,
        days=days,
        min_violation_count=min_violation_count,
    )

