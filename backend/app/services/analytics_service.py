from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.models.enums import ViolationStatus
from app.models.violation import Violation
from app.schemas.analytics import (
    AnalyticsResponse,
    CountByCamera,
    CountByStatus,
    CountByType,
    TrendPoint,
)


class AnalyticsService:
    @staticmethod
    def get_analytics(db: Session, days: int = 30) -> AnalyticsResponse:
        since = datetime.now(UTC) - timedelta(days=days)
        filters = [Violation.detected_at >= since]

        total = db.scalar(select(func.count(Violation.id)).where(*filters)) or 0
        status_counts = dict(
            db.execute(
                select(Violation.status, func.count(Violation.id))
                .where(*filters)
                .group_by(Violation.status)
            ).all()
        )

        by_type = [
            CountByType(violation_type=str(row[0]), count=row[1])
            for row in db.execute(
                select(Violation.violation_type, func.count(Violation.id))
                .where(*filters)
                .group_by(Violation.violation_type)
                .order_by(func.count(Violation.id).desc())
            ).all()
        ]

        by_status = [
            CountByStatus(status=str(status), count=count)
            for status, count in status_counts.items()
        ]

        by_camera = [
            CountByCamera(
                camera_id=row.camera_id,
                camera_name=row.camera_name or "Unassigned camera",
                location_name=row.location_name or "Unknown location",
                count=row.count,
            )
            for row in db.execute(
                select(
                    Violation.camera_id.label("camera_id"),
                    Camera.name.label("camera_name"),
                    Camera.location_name.label("location_name"),
                    func.count(Violation.id).label("count"),
                )
                .outerjoin(Camera, Violation.camera_id == Camera.id)
                .where(*filters)
                .group_by(Violation.camera_id, Camera.name, Camera.location_name)
                .order_by(func.count(Violation.id).desc())
            ).all()
        ]

        detected_day = func.date(Violation.detected_at)
        trend = [
            TrendPoint(date=row.day, count=row.count)
            for row in db.execute(
                select(
                    detected_day.label("day"),
                    func.count(Violation.id).label("count"),
                )
                .where(*filters)
                .group_by(detected_day)
                .order_by(detected_day)
            ).all()
        ]

        return AnalyticsResponse(
            total_violations=total,
            pending_review=status_counts.get(ViolationStatus.PENDING_REVIEW, 0),
            confirmed=status_counts.get(ViolationStatus.CONFIRMED, 0),
            rejected=status_counts.get(ViolationStatus.REJECTED, 0),
            by_type=by_type,
            by_status=by_status,
            by_camera=by_camera,
            trend=trend,
        )
