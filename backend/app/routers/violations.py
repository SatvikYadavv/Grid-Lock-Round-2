from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.enums import ViolationStatus, ViolationType
from app.schemas.violation import ViolationListResponse, ViolationRead
from app.services.violation_service import ViolationService


router = APIRouter(tags=["violations"])


@router.get("/violations", response_model=ViolationListResponse)
def list_violations(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    violation_type: ViolationType | None = Query(default=None),
    status: ViolationStatus | None = Query(default=None),
    camera_id: UUID | None = Query(default=None),
    plate_number: str | None = Query(default=None, min_length=2, max_length=32),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
) -> ViolationListResponse:
    items, total = ViolationService.list_violations(
        db,
        limit=limit,
        offset=offset,
        violation_type=violation_type,
        status=status,
        camera_id=camera_id,
        plate_number=plate_number,
        start_date=start_date,
        end_date=end_date,
    )
    return ViolationListResponse(total=total, limit=limit, offset=offset, items=items)


@router.get("/violations/{id}", response_model=ViolationRead)
def get_violation(
    id: UUID = Path(...),
    db: Session = Depends(get_db),
) -> ViolationRead:
    return ViolationService.get_violation(db, id)
