from enum import StrEnum


class CameraStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class ZoneType(StrEnum):
    ALLOWED_DIRECTION = "allowed_direction"
    NO_PARKING = "no_parking"
    DETECTION_AREA = "detection_area"


class ImageProcessingStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ObjectType(StrEnum):
    MOTORCYCLE = "motorcycle"
    RIDER = "rider"
    HELMET = "helmet"
    NO_HELMET = "no_helmet"
    CAR = "car"
    TRUCK = "truck"
    BUS = "bus"
    LICENSE_PLATE = "license_plate"
    UNKNOWN = "unknown"


class ViolationType(StrEnum):
    HELMET_NON_COMPLIANCE = "helmet_non_compliance"
    TRIPLE_RIDING = "triple_riding"
    WRONG_SIDE_DRIVING = "wrong_side_driving"
    ILLEGAL_PARKING = "illegal_parking"


class ViolationStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"

