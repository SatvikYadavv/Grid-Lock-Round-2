import re
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config.settings import settings
from app.utils.exceptions import StorageError, ValidationError


@dataclass(frozen=True)
class StoredFile:
    file_name: str
    original_filename: str
    content_type: str
    file_size_bytes: int
    path: Path
    url: str


class StorageService:
    def __init__(self, upload_dir: Path | None = None) -> None:
        self.upload_dir = upload_dir or settings.upload_dir

    async def save_upload(self, file: UploadFile) -> StoredFile:
        self._validate_upload_metadata(file)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        original_filename = Path(file.filename or "traffic-image").name
        suffix = self._suffix_for(file.content_type, original_filename)
        safe_stem = self._safe_stem(original_filename)
        file_name = f"{safe_stem}-{uuid4().hex}{suffix}"
        destination = self.upload_dir / file_name

        size = 0
        try:
            with destination.open("wb") as output:
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    if size > settings.max_upload_bytes:
                        output.close()
                        destination.unlink(missing_ok=True)
                        raise ValidationError(
                            f"Image is larger than the {settings.max_upload_mb} MB limit.",
                            details={"max_upload_mb": settings.max_upload_mb},
                        )
                    output.write(chunk)
        except ValidationError:
            raise
        except OSError as exc:
            raise StorageError("Failed to store uploaded image.") from exc

        if size == 0:
            destination.unlink(missing_ok=True)
            raise ValidationError("Uploaded image is empty.")

        return StoredFile(
            file_name=file_name,
            original_filename=original_filename,
            content_type=file.content_type or "application/octet-stream",
            file_size_bytes=size,
            path=destination,
            url=f"/uploads/{file_name}",
        )

    def delete_file(self, path: Path) -> None:
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            raise StorageError("Failed to delete stored image.") from exc

    @staticmethod
    def _safe_stem(filename: str) -> str:
        stem = Path(filename).stem.lower()
        stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
        return stem[:60] or "traffic-image"

    @staticmethod
    def _suffix_for(content_type: str | None, filename: str) -> str:
        configured = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }
        if content_type in configured:
            return configured[content_type]
        suffix = Path(filename).suffix.lower()
        return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp"} else ".jpg"

    @staticmethod
    def _validate_upload_metadata(file: UploadFile) -> None:
        if not file.filename:
            raise ValidationError("Uploaded image must include a filename.")
        if file.content_type not in settings.allowed_image_types:
            raise ValidationError(
                "Unsupported image type.",
                details={
                    "content_type": file.content_type,
                    "allowed_image_types": settings.allowed_image_types,
                },
            )

