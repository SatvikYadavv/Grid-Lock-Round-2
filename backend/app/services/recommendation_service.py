from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.models.enums import ViolationStatus, ViolationType
from app.models.violation import Violation
from app.schemas.recommendation import Recommendation, RecommendationResponse


class RecommendationService:
    @staticmethod
    def get_recommendations(
        db: Session,
        *,
        days: int = 30,
        min_violation_count: int = 3,
    ) -> RecommendationResponse:
        since = datetime.now(UTC) - timedelta(days=days)
        filters = [Violation.detected_at >= since]

        total = db.scalar(select(func.count(Violation.id)).where(*filters)) or 0
        recommendations: list[Recommendation] = []

        hotspot_rows = db.execute(
            select(
                Violation.camera_id,
                Camera.name,
                Camera.location_name,
                Violation.violation_type,
                func.count(Violation.id).label("count"),
            )
            .outerjoin(Camera, Violation.camera_id == Camera.id)
            .where(*filters)
            .group_by(Violation.camera_id, Camera.name, Camera.location_name, Violation.violation_type)
            .having(func.count(Violation.id) >= min_violation_count)
            .order_by(func.count(Violation.id).desc())
            .limit(10)
        ).all()

        for row in hotspot_rows:
            recommendations.append(
                RecommendationService._recommend_for_hotspot(
                    camera_id=row.camera_id,
                    camera_name=row.name,
                    location_name=row.location_name,
                    violation_type=row.violation_type,
                    count=row.count,
                )
            )

        pending = db.scalar(
            select(func.count(Violation.id)).where(
                Violation.detected_at >= since,
                Violation.status == ViolationStatus.PENDING_REVIEW,
            )
        ) or 0
        if pending >= min_violation_count:
            recommendations.append(
                Recommendation(
                    id=f"review-backlog-{uuid4().hex[:8]}",
                    priority="medium",
                    title="Reduce pending violation review backlog",
                    description=f"{pending} violations are waiting for review in the selected window.",
                    estimated_impact="Faster confirmation and cleaner enforcement reporting.",
                )
            )

        return RecommendationResponse(
            generated_from_violations=total,
            recommendations=recommendations,
        )

    @staticmethod
    def _recommend_for_hotspot(
        *,
        camera_id,
        camera_name: str | None,
        location_name: str | None,
        violation_type: ViolationType,
        count: int,
    ) -> Recommendation:
        title_by_type = {
            ViolationType.HELMET_NON_COMPLIANCE: "Increase helmet compliance enforcement",
            ViolationType.TRIPLE_RIDING: "Target two-wheeler occupancy violations",
            ViolationType.WRONG_SIDE_DRIVING: "Add wrong-side driving deterrence",
            ViolationType.ILLEGAL_PARKING: "Strengthen no-parking controls",
        }
        description_by_type = {
            ViolationType.HELMET_NON_COMPLIANCE: "Deploy signage and officer review during peak two-wheeler movement.",
            ViolationType.TRIPLE_RIDING: "Prioritize rider-count violations near the camera location.",
            ViolationType.WRONG_SIDE_DRIVING: "Review lane markings, barricades, and directional signage near the hotspot.",
            ViolationType.ILLEGAL_PARKING: "Add visible no-parking markers and periodic towing patrols.",
        }
        priority = "high" if count >= 10 else "medium"
        location = location_name or "Unknown location"

        return Recommendation(
            id=f"{violation_type}-{camera_id or 'unassigned'}-{uuid4().hex[:8]}",
            priority=priority,
            title=title_by_type[violation_type],
            description=f"{count} {violation_type.value.replace('_', ' ')} cases were detected at {location}. "
            f"{description_by_type[violation_type]}",
            camera_id=camera_id,
            camera_name=camera_name or "Unassigned camera",
            location_name=location_name or "Unknown location",
            violation_type=violation_type,
            estimated_impact="Focused enforcement at a recurring hotspot.",
        )

