from app.database.base import Base
from app.models.camera import Camera, CameraZone
from app.models.detection import Detection, OCRResult
from app.models.image import UploadedImage
from app.models.violation import Violation, ViolationEvidence

__all__ = [
    "Base",
    "Camera",
    "CameraZone",
    "Detection",
    "OCRResult",
    "UploadedImage",
    "Violation",
    "ViolationEvidence",
]

