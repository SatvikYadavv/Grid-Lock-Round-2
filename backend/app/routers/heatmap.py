from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.enums import ViolationType
from app.schemas.heatmap import HeatmapResponse
from app.services.heatmap_service import HeatmapService


router = APIRouter(tags=["heatmap"])


@router.get("/heatmap", response_model=HeatmapResponse)
def get_heatmap(
    days: int = Query(default=30, ge=1, le=365),
    violation_type: ViolationType | None = Query(default=None),
    db: Session = Depends(get_db),
) -> HeatmapResponse:
    return HeatmapService.get_heatmap(db, days=days, violation_type=violation_type)

