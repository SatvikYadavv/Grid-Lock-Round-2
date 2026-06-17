from datetime import datetime
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, joinedload

from app.models.enums import ViolationStatus, ViolationType
from app.models.violation import Violation
from app.utils.exceptions import NotFoundError, ValidationError


class ViolationService:
    @staticmethod
    def list_violations(
        db: Session,
        *,
        limit: int,
        offset: int,
        violation_type: ViolationType | None = None,
        status: ViolationStatus | None = None,
        camera_id: UUID | None = None,
        plate_number: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> tuple[list[Violation], int]:
        if start_date and end_date and start_date > end_date:
            raise ValidationError("start_date must be before end_date.")

        filters = []
        if violation_type:
            filters.append(Violation.violation_type == violation_type)
        if status:
            filters.append(Violation.status == status)
        if camera_id:
            filters.append(Violation.camera_id == camera_id)
        if plate_number:
            filters.append(Violation.plate_number.ilike(f"%{plate_number.strip()}%"))
        if start_date:
            filters.append(Violation.detected_at >= start_date)
        if end_date:
            filters.append(Violation.detected_at <= end_date)

        count_statement = select(func.count(Violation.id)).where(*filters)
        total = db.scalar(count_statement) or 0

        statement: Select[tuple[Violation]] = (
            select(Violation)
            .options(
                joinedload(Violation.camera),
                joinedload(Violation.image),
                joinedload(Violation.evidence),
            )
            .where(*filters)
            .order_by(Violation.detected_at.desc())
            .limit(limit)
            .offset(offset)
        )
        violations = db.execute(statement).unique().scalars().all()
        return list(violations), total

    @staticmethod
    def get_violation(db: Session, violation_id: UUID) -> Violation:
        statement = (
            select(Violation)
            .options(
                joinedload(Violation.camera),
                joinedload(Violation.image),
                joinedload(Violation.evidence),
            )
            .where(Violation.id == violation_id)
        )
        violation = db.execute(statement).unique().scalar_one_or_none()
        if not violation:
            raise NotFoundError("Violation not found.", details={"violation_id": str(violation_id)})
        return violation

