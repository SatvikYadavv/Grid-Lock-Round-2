from dataclasses import dataclass, field
from pathlib import Path

from app.config.settings import settings
from app.models.enums import ObjectType, ViolationType
from app.utils.logging import get_logger


logger = get_logger(__name__)


@dataclass(frozen=True)
class DetectionPayload:
    object_type: ObjectType
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float
    track_id: str | None = None
    metadata: dict | None = None


@dataclass(frozen=True)
class OCRPayload:
    plate_number: str
    confidence: float
    cropped_plate_url: str | None = None


@dataclass(frozen=True)
class EvidencePayload:
    evidence_image_url: str
    cropped_vehicle_url: str | None = None
    annotated_image_url: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class ViolationPayload:
    violation_type: ViolationType
    confidence: float
    vehicle_type: str | None = None
    plate_number: str | None = None
    evidence: list[EvidencePayload] = field(default_factory=list)


@dataclass(frozen=True)
class PipelineResult:
    detections: list[DetectionPayload] = field(default_factory=list)
    ocr_results: list[OCRPayload] = field(default_factory=list)
    violations: list[ViolationPayload] = field(default_factory=list)


class AIPipelineService:
    """Adapter boundary for YOLOv8, OpenCV, EasyOCR, and violation rules."""

    def process(self, image_path: Path) -> PipelineResult:
        if not settings.ai_processing_enabled:
            logger.info("AI processing disabled; image stored without inference.", extra={"image": str(image_path)})
            return PipelineResult()

        if not settings.yolo_model_path:
            logger.warning("AI processing enabled but YOLO_MODEL_PATH is not configured.")
            return PipelineResult()

        logger.warning(
            "AI adapter is ready for a trained YOLOv8 model, but project-specific "
            "violation inference has not been enabled in this scaffold."
        )
        return PipelineResult()

