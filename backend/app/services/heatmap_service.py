from collections import defaultdict
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.models.enums import ViolationType
from app.models.violation import Violation
from app.schemas.heatmap import HeatmapPoint, HeatmapResponse


class HeatmapService:
    @staticmethod
    def get_heatmap(
        db: Session,
        *,
        days: int = 30,
        violation_type: ViolationType | None = None,
    ) -> HeatmapResponse:
        since = datetime.now(UTC) - timedelta(days=days)
        filters = [Violation.detected_at >= since]
        if violation_type:
            filters.append(Violation.violation_type == violation_type)

        rows = db.execute(
            select(
                Camera.id.label("camera_id"),
                Camera.name.label("camera_name"),
                Camera.location_name.label("location_name"),
                Camera.latitude.label("latitude"),
                Camera.longitude.label("longitude"),
                Violation.violation_type.label("violation_type"),
                func.count(Violation.id).label("count"),
            )
            .join(Violation, Violation.camera_id == Camera.id)
            .where(*filters)
            .group_by(
                Camera.id,
                Camera.name,
                Camera.location_name,
                Camera.latitude,
                Camera.longitude,
                Violation.violation_type,
            )
        ).all()

        grouped: dict[str, dict] = {}
        type_counts: dict[str, dict[str, int]] = defaultdict(dict)
        for row in rows:
            key = str(row.camera_id)
            grouped.setdefault(
                key,
                {
                    "camera_id": row.camera_id,
                    "camera_name": row.camera_name,
                    "location_name": row.location_name,
                    "latitude": row.latitude,
                    "longitude": row.longitude,
                    "intensity": 0,
                },
            )
            grouped[key]["intensity"] += row.count
            type_counts[key][str(row.violation_type)] = row.count

        points = []
        for key, item in grouped.items():
            dominant = max(type_counts[key].items(), key=lambda entry: entry[1])[0] if type_counts[key] else None
            points.append(HeatmapPoint(**item, dominant_violation_type=dominant))

        points.sort(key=lambda point: point.intensity, reverse=True)
        return HeatmapResponse(total_points=len(points), points=points)

