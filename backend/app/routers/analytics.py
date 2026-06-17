from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import AnalyticsService


router = APIRouter(tags=["analytics"])


@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
) -> AnalyticsResponse:
    return AnalyticsService.get_analytics(db, days=days)

