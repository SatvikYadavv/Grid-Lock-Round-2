from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService


router = APIRouter(tags=["upload"])
upload_service = UploadService()


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    camera_id: UUID | None = Form(default=None),
    captured_at: datetime | None = Form(default=None),
    db: Session = Depends(get_db),
) -> UploadResponse:
    image, detected_violations = await upload_service.upload_image(
        db=db,
        file=file,
        camera_id=camera_id,
        captured_at=captured_at,
    )
    return UploadResponse(
        id=image.id,
        camera_id=image.camera_id,
        image_url=image.image_url,
        original_filename=image.original_filename,
        content_type=image.content_type,
        file_size_bytes=image.file_size_bytes,
        processing_status=image.processing_status,
        captured_at=image.captured_at,
        detected_violations=detected_violations,
    )

